# File: views.py
# Author: Jared Chou (jchou@bu.edu) 2024
# Description: Define custom views that will display and process data for the user to interact with. 

from django.shortcuts import render, redirect
from django.views.generic import *
from . models import *
from . forms import *
from . mixins import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.base import ContextMixin
from urllib.parse import urlencode
import plotly
import plotly.graph_objs as go

# trip related views
class ShowAllTripsView(UserDetailsMixin, ListView):
    '''view that displays all trips'''
    model = Trip
    context_object_name = "trips"
    template_name = "project/show_all_trips.html"
    
    def get_context_data(self, **kwargs):
        '''set context variables for reference in html templates'''
        context = super().get_context_data(**kwargs)
        # define the 'action_url' variable which is used to display the correct page after filtering
        # objects based on the user's input
        context['action_url'] = "show_all_trips"
        return context
    
    def get_queryset(self):
        '''filter the set of trips shown based on parameters'''
        
        # first get the set of all Trip objects and order them based on start_date
        trips = super().get_queryset().order_by("start_date").reverse()
        
        # iterate over query variables in the GET request to filter the queryset based on parameters
        for param in self.request.GET:
            value = self.request.GET[param] # define the value of the parameter
            print(f'searching for trips with {param} = {value}')
            
            if value != "": # ensure that an actual value is actually passed for processing
                match param:
                    case "name": # filter based on trip name
                        trips = trips.filter(name__contains=value)
                    case "destination": # filter based on trip destination
                        trips = trips.filter(destination__contains=value)
                    case "start_date": # filter based on trip start date
                        # first parse the input
                        vals = value.split('-')
                        trips = trips.filter(start_date__year=vals[0], start_date__month=vals[1], start_date__day=vals[2])
                    case "end_date": # filter based on trip end date
                        vals = value.split('-')
                        trips = trips.filter(end_date__year=vals[0], end_date__month=vals[1], end_date__day=vals[2])
        return trips
    
class ShowTripView(UserDetailsMixin, DetailView):
    '''a view that displays a single trip'''
    model = Trip
    context_object_name = "trip"
    template_name = "project/show_trip.html"
    
    def get_context_data(self, **kwargs):
        '''context variables for displaying trip details'''
        context = super().get_context_data(**kwargs)
        
        # Define the 'is_attendee' context variable that hides UI elements if the user should not have
        # access to those operations. Users must be authenticated and a trip attendee to access these 
        # UI elements
        if context['logged_in_profile'] != None and context['logged_in_profile'] in self.get_object().get_attendees():
            # this means a user is logged in
            context['is_attendee'] = True
        else:
            context['is_attendee'] = False
        
        return context
    
class CreateTripView(UserDetailsMixin, CreateView):
    '''view to create a new trip'''
    form_class = CreateTripForm
    template_name = "project/create_trip.html"
    
    def form_valid(self, form):
        '''define custom behavior to add the creating user to a new trip'''
        
        trip = form.save() # create the trip
        profile = self.get_user_profile(self.request.user) # get the profile of the current user
            
        # attach the current user as an attendee and save the new trip object
        attend_trip = AttendTrip(trip=trip, profile=profile)
        attend_trip.save()
        
        # show the newly created trip
        return redirect('show_trip', pk=trip.pk)
    
class DeleteTripView(AttendeeRequiredTripMixin, DeleteView):
    '''view to delete an existing trip'''
    model = Trip
    template_name = "project/delete_trip.html"
    
    def get_success_url(self):
        '''success url after successful deletion'''
        return reverse('show_all_trips')
    
    def get_login_url(self):
        '''login url if unauthorized'''
        return super().get_login_url()
    
class UpdateTripView(AttendeeRequiredTripMixin, UpdateView):
    '''view to update an existing trip'''
    model = Trip
    form_class = UpdateTripForm
    template_name = "project/update_trip.html"
    context_object_name = "trip"
    
    def get_success_url(self):
        '''redirect URL after successful update to show the trip that was just updated'''
        self.kwargs['pk'] = self.get_context_data()['object'].pk
        return reverse('show_trip', kwargs = self.kwargs)
      
# cost related views  
class CreateCostView(AttendeeRequiredTripMixin, AssociatedTripMixin, CreateView):
    '''view to create a new cost'''
    form_class = CreateCostForm
    template_name = "project/create_cost.html"
    
    def form_valid(self, form):
        '''create a new cost based on a valid form submission'''
        
        # set form.instance.actual_cost based on the 'paid_by' input
        if (form.instance.paid_by == None or form.instance.paid_by == ''):
            # if paid by is empty, this is a planned cost, not an actual cost
            form.instance.actual_cost = False
        else:
            form.instance.actual_cost = True
            
        # get the trip associated with this cost to set the foreign key
        trip = Trip.objects.get(pk=self.kwargs['trip_pk'])
        form.instance.trip = trip
        
        return super().form_valid(form)
    
class UpdateCostView(AttendeeRequiredTripMixin, AssociatedTripMixin, UpdateView):
    '''View to allow users to update parameters of costs on the trip. POST requests will be directly
    made to this view from the ShowTripView when users update the cost fields directly in
    the ShowTripView.
    '''
    model = Cost
    form_class = UpdateCostForm
    template_name = 'project/update_cost.html'
     
    def form_valid(self, form):
        '''process update forms and update the object with the new inputs'''
        
        print(f'this is the cost we are updating with: {form.instance}')
        
        # update actual_cost if the cost was paid or not paid by someone
        if form.instance.paid_by == None or form.instance.paid_by == '':
            form.instance.actual_cost = False
        else:
            form.instance.actual_cost = True
        
        return super().form_valid(form)
    
class DeleteCostView(AttendeeRequiredTripMixin, AssociatedTripMixin, View):
    '''View to delete a cost directly.'''
    
    def dispatch(self, request, *args, **kwargs):
        '''function to handle the immediate deletion of a cost'''

        # delete the cost associated with the pk provided in kwargs
        cost = Cost.objects.get(pk=self.kwargs['pk'])
        cost.delete()
        
        # show the trip that the cost was associated with
        return redirect('show_trip', pk=self.kwargs['trip_pk'])
    
# attendee related views
class AddAttendeeToTripView(AttendeeRequiredTripMixin, AssociatedTripMixin, CreateView):
    '''view to add a new attendee to a trip'''
    form_class = AddAttendeeToTripForm
    template_name = 'project/add_attendee_to_trip.html'
    
    def get_form(self, form_class=None):
        '''return an instance of the form to be displayed'''
        # Get the trip that the user wants to add an attendee to
        trip = Trip.objects.get(pk=self.kwargs['trip_pk'])  
        # Filter the profiles displayed in the form to only include profiles that are not already 
        # attending the trip.
        attendee_options = Profile.objects.all().exclude(id__in=trip.get_attendees().values('id'))
        # Pass these attendee_options to the form so it only displays Profiles that are not attendees
        # of the trip as options for Profiles to add as trip attendees.
        return AddAttendeeToTripForm(attendee_options=attendee_options, **self.get_form_kwargs())
    
    def form_valid(self, form):
        '''process form upon submission'''
        trip = Trip.objects.get(pk=self.kwargs['trip_pk'])
        form.instance.trip = trip    

        # check that this profile hasn't been added to the trip already
        attendees = trip.get_attendees()
        if form.instance.profile in attendees:
            # if the profile is already an attendee, redirect back to the ShowTripView
            print(f'the profie {form.instance.profile} is already attending the trip {trip}')
            return redirect('show_trip', pk=trip.pk)
        else:
            # if the profile is not an attendee, proceed with adding the profile as a new trip attendee
            print(f'adding new attendee {form.instance.profile}')
            return super().form_valid(form)
    
class RemoveAttendeesView(AttendeeRequiredTripMixin, DetailView):
    '''View to display the list of attendees, allowing users to remove attendees from the trip.'''
    model = Trip
    template_name = "project/remove_attendees.html"
    context_object_name = "trip"
    
class RemoveAttendeeView(View):
    '''View to remove a user from a trip. Does not display a confirmation page.'''
    def dispatch(self, request, *args, **kwargs):
        '''view to remove an attendee from the trip'''
        
        # get the specified trip and profile based on kwargs passed from the URL
        trip = Trip.objects.get(pk=self.kwargs['trip_pk'])
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        
        # get and delete all AttendTrip objects associating the profile as an attendee to the trip
        attendee_relations = AttendTrip.objects.filter(trip=trip) & AttendTrip.objects.filter(profile=profile)
        for r in attendee_relations:
            r.delete()
        
        # redirect to display the RemoveAttendeesView
        return redirect('remove_attendees', pk=self.kwargs['trip_pk'])
    
class JoinTripView(UserDetailsMixin, View):
    '''view to process users joining an existing trip'''
    def dispatch(self, request, *args, **kwargs):
        '''process adding the current user to a trip'''

        # get the trip that the user is trying to join
        trip = Trip.objects.get(pk=self.kwargs['pk'])

        if request.user.is_authenticated :
            # first check that there is a user authenticated
            profile = self.get_user_profile(request.user)
            
            # add this user as an attendee            
            attend_trip = AttendTrip(trip=trip, profile=profile)
            attend_trip.save()
            
            # show the trip that the user just joined
            return redirect('show_trip', pk=self.kwargs['pk'])
        else:
            # if the user isn't authenticated, then the user must sign in first
            # make sure to redirect with a next url assigned to redirect the user after they sign in
            return redirect(encode_url('login', {'next': reverse('join_trip', kwargs={'pk': trip.pk})}))
        
class LeaveTripView(UserDetailsMixin, DetailView):
    '''View to process a trip attendee leaving the trip. Display the confirmation page before deletion.'''
    model = Trip
    template_name = "project/delete_attend_trip.html"
    context_object_name = "trip"
    
    def post(self, request, *args, **kwargs):
        '''handle post requests to remove the current user from a trip'''

        # get the trip and profile 
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        profile = self.get_user_profile(request.user)
        
        # get and delete all AttendTrip objects that associate this profile as an attendee of the trip
        attendee_relations = AttendTrip.objects.filter(trip=trip) & AttendTrip.objects.filter(profile=profile)
        for r in attendee_relations:
            r.delete()
        
        # display the trip that the user just left
        return redirect('show_trip', pk=self.kwargs['pk'])
        
# image related views 
class CreateImageView(AttendeeRequiredTripMixin, AssociatedTripMixin, CreateView):
    '''view to create a new image'''
    form_class = CreateImageForm
    template_name = "project/create_image.html"
    
    def form_valid(self, form):
        '''process successful form submission'''
        context = self.get_context_data() # get context data from superclasses
        
        # get the trip associated with this image
        trip = Trip.objects.get(pk=context["trip_pk"])
        
        # get the user that posted this image and ensure that the poster is an attendee of the trip
        user_profile = context['logged_in_profile']
        
        # set the foreign keys for the image
        form.instance.trip = trip
        form.instance.poster = user_profile
        
        return super().form_valid(form)

class DeleteImageView(AttendeeRequiredTripMixin, AssociatedTripMixin, DeleteView):
    '''deletion page for images with confirmation message'''
    model = Image
    template_name = "project/delete_image.html"
    context_object_name = "image"
    
# profile related views
class CreateProfileView(CreateView):
    '''view to create a new profile and user for the app'''
    form_class = CreateProfileForm
    template_name = "project/create_profile.html"
    
    def get_context_data(self, **kwargs):
        '''define context variables
        Also includes definition of a UserCreationForm to create both a new django user and a 
        Profile at the same time     
        '''
        
        # get context data from superclass
        context = super().get_context_data(**kwargs)
        
        # add a UserCreationForm to the context data to be rendered
        user_creation_form = UserCreationForm(self.request.POST)
        context['UserCreationForm'] = user_creation_form
        
        # return updated context data
        return context

    def form_valid(self, form):
        '''process successful submission of the profile creation form'''
        
        # initialize the UserCreationForm with the information provided by the user
        userform = UserCreationForm(self.request.POST)
        
        # if the userform data is not valid, redirect the user back to the form while showing the 
        # error messages
        if not userform.is_valid():
            # errors in creating django user, return with errors
            return self.render_to_response(self.get_context_data(form=form, UserCreationForm=userform))
        
        # if the django user creation form was valid, create the user and log in the user
        user = userform.save()
        login(self.request, user)
        
        # attach this newly created user to the form
        form.instance.user = user
        return super().form_valid(form)
    
    def get_success_url(self):
        '''redirect URL after a new user is created to ShowAllTripsView'''
        return reverse('show_all_trips')    
        
class NoAccessView(TemplateView):
    '''view to display a no access page based on the provided template'''
    template_name = "project/no_access.html"
        
class CostBreakdownView(UserDetailsMixin, ListView):
    '''view to display graphs breaking down the different costs'''
    model = Cost
    template_name = "project/cost_breakdown.html"
    
    def get_queryset(self):
        '''limit set of costs to costs applicable to this trip'''
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        return Cost.objects.filter(trip=trip)
    
    def get_context_data(self, **kwargs):
        '''generate graphs and add to context data'''
        context = super().get_context_data(**kwargs) # get context data from superclass
        
        # get the list of all costs associated with this trip
        costs = self.get_queryset()
        cost_paid_by = {}
        
        # iterate over costs to calculate how much each individual paid throughout the trip
        for c in costs:
            # ensure the cost is an actual cost and not a planned cost before including its price
            if c.actual_cost:
                # get the string representation of the profile that paid for this cost
                paid_by = str(c.paid_by)
                # increment the dictionary to track that this cost was paid for by this Profile
                if paid_by in cost_paid_by:
                    cost_paid_by[paid_by] += c.item_price
                else:
                    cost_paid_by[paid_by] = c.item_price
        
        # generate Pie chart to display the breakdown of costs based on who paid for what
        fig = go.Pie(values=list(cost_paid_by.values()), labels=list(cost_paid_by.keys()))
        graph_cost_breakdown = plotly.offline.plot({
            "data":[fig], 
            "layout_title_text": "Cost Breakdown"
        }, auto_open=False,
        output_type="div")
        
        # add graph to context data to be rendered and return context data
        context['graph_cost_breakdown'] = graph_cost_breakdown
        return context  