from django.shortcuts import render, redirect
from django.views.generic import *
from . models import *
from . forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.base import ContextMixin
from urllib.parse import urlencode

# custom mixins
class UserDetailsMixin(object):
    '''class to share sign in details'''    
    def get_user_profile(self, user):
        '''get a profile from a user'''
        return Profile.objects.filter(user=user).first()
    
    def get_context_data(self, **kwargs):
        '''update the context data to include'''
        # find user who is logged in
        # print(f'request:{self.request.user}')
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # find profile 
            # add to context data
            profile = self.get_user_profile(self.request.user)
            context['logged_in_profile'] = profile
        else: 
            context['logged_in_profile'] = None

        return context
    
class AssociatedTripMixin():
    '''mixin to represent shared behavior for views that require relationships to a specific trip'''
    def get_context_data(self, **kwargs):
        '''add primary key of the associated trip'''
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        return context
    
    def get_success_url(self):
        '''redirect url to the trip that the newly created object is attached to'''
        return reverse('show_trip', kwargs={"pk":self.kwargs["trip_pk"]})

# views
class ShowAllTripsView(UserDetailsMixin, ListView):
    '''view that displays all trips'''
    model = Trip
    context_object_name = "trips"
    template_name = "project/show_all_trips.html"
    
    def get_context_data(self, **kwargs):
        '''set context variables'''
        context = super().get_context_data(**kwargs)
        # parameters to search for in a trip
        context['action_url'] = "show_all_trips"
                
        return context
    
    def get_queryset(self):
        '''filter the set of trips shown based on parameters'''
        trips = super().get_queryset().order_by("start_date").reverse()
        
        for param in self.request.GET:
            value = self.request.GET[param]
            print(f'searching for trips with {param} = {value}')
            
            if value != "":
                match param:
                    case "name":
                        trips = trips.filter(name__contains=value)
                    case "destination":
                        trips = trips.filter(destination__contains=value)
                    case "start_date":
                        # first parse the input
                        vals = value.split('-')
                        trips = trips.filter(start_date__year=vals[0], start_date__month=vals[1], start_date__day=vals[2])
                    case "end_date":
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
        
        if context['logged_in_profile'] != None and context['logged_in_profile'] in self.get_object().get_attendees():
            # this means a user is logged in
            context['is_attendee'] = True
        else:
            context['is_attendee'] = False
        
        return context
    
class CreateTripView(CreateView):
    '''view to create a new trip'''
    form_class = CreateTripForm
    template_name = "project/create_trip.html"
    
class DeleteTripView(UserDetailsMixin, DeleteView):
    '''view to delete an existing trip'''
    model = Trip
    template_name = "project/delete_trip.html"
    
    def get_success_url(self):
        return reverse('show_all_trips')
    
class UpdateTripView(UserDetailsMixin, UpdateView):
    '''view to update an existing trip'''
    model = Trip
    form_class = UpdateTripForm
    template_name = "project/update_trip.html"
    context_object_name = "trip"
    
    def get_success_url(self):
        '''redirect URL after successful update'''
        self.kwargs['pk'] = self.get_context_data()['object'].pk
        return reverse('show_trip', kwargs = self.kwargs)
        
class CreateCostView(UserDetailsMixin, AssociatedTripMixin, CreateView):
    '''view to create a new cost'''
    form_class = CreateCostForm
    template_name = "project/create_cost.html"
    
    def form_valid(self, form):
        '''create a new cost based on a valid form submission'''
        if (form.instance.paid_by == None):
            # if paid by is empty, this is a planned cost, not an actual cost
            form.instance.actual_cost = False
        else:
            form.instance.actual_cost = True
            
        # get the trip
        trip = Trip.objects.get(pk=self.kwargs['trip_pk'])
        form.instance.trip = trip
        
        return super().form_valid(form)
    
class UpdateCostView(UserDetailsMixin, AssociatedTripMixin, UpdateView):
    '''view to allow users to update parameters of costs on the trip'''
    model = Cost
    form_class = UpdateCostForm
    template_name = 'project/update_cost.html'
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        
        return super().post(request, *args, **kwargs)
    
class DeleteCostView(UserDetailsMixin, AssociatedTripMixin, View):
    '''view to delete a new cost'''
    def dispatch(self, request, *args, **kwargs):
        '''function to handle the immediate deletion of a cost'''
        print(f'we are trying to delete a cost')
        
        print(self.kwargs)
        cost = Cost.objects.get(pk=self.kwargs['pk'])
        
        cost.delete()
        return redirect('show_trip', pk=self.kwargs['trip_pk'])
    
    
class AddAttendeeToTripView(UserDetailsMixin, AssociatedTripMixin, CreateView):
    '''view to add a new attendee to a trip'''
    form_class = AddAttendeeToTripForm
    template_name = 'project/add_attendee_to_trip.html'
    
    def form_valid(self, form):
        '''process form upon submission'''
        trip = Trip.objects.get(pk=self.kwargs['trip_pk'])
        form.instance.trip = trip    
        
        # check that this profile hasn't been added to the trip already
        attendees = trip.get_attendees()
        if form.instance.profile in attendees:
            print(f'the profie {form.instance.profile} is already attending the trip {trip}')
            return redirect('show_trip', pk=trip.pk)
        else:
            return super().form_valid(form)
    
class RemoveAttendeesView(UserDetailsMixin, DetailView):
    '''view to display the list of attendees to enable removal'''
    model = Trip
    template_name = "project/remove_attendees.html"
    context_object_name = "trip"
    
    def get_context_data(self, **kwargs):
        '''update context variables to include the signed in user'''
        self.kwargs['trip_pk'] = self.kwargs['pk']
        return super().get_context_data(**kwargs)
    
class RemoveAttendeeView(View):
    '''view to remove a user from a trip'''
    def dispatch(self, request, *args, **kwargs):
        '''view to remove an attendee from the trip'''
        trip = Trip.objects.get(pk=self.kwargs['trip_pk'])
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        
        attendee_relations = AttendTrip.objects.filter(trip=trip) & AttendTrip.objects.filter(profile=profile)
        
        for r in attendee_relations:
            r.delete()
        
        return redirect('remove_attendees', pk=self.kwargs['trip_pk'])
    
class JoinTripView(UserDetailsMixin, View):
    '''view to process users joining an existing trip'''
    def dispatch(self, request, *args, **kwargs):
        '''process adding the current user to a trip'''

        if request.user.is_authenticated :
            # first check that there is a user authenticated
            profile = self.get_user_profile(request.user)
            
            # add this user as an attendee
            trip = Trip.objects.get(pk=self.kwargs['pk'])
            
            attend_trip = AttendTrip(trip=trip, profile=profile)
            attend_trip.save()
            
            return redirect('show_trip', pk=self.kwargs['pk'])
        else:
            
            # make sure to redirect with a next url assigned
            base_url = reverse('login')
            query_str = urlencode({'next': reverse('show_trip', kwargs={'pk': 1})})
            url = '{}?{}'.format(base_url, query_str)
            return redirect(url)
    
class CreateImageView(UserDetailsMixin, AssociatedTripMixin, CreateView):
    '''view to create a new image'''
    form_class = CreateImageForm
    template_name = "project/create_image.html"
    
    def form_valid(self, form):
        '''process successful form submission'''
        context = self.get_context_data()
        print(f"in form valid with context: {context}")
        
        # get the trip associated with this image
        trip = Trip.objects.get(pk=context["trip_pk"])
        
        # get the user that posted this image and ensure that the poster is an attendee of the trip
        user_profile = context['logged_in_profile']
        
        form.instance.trip = trip
        form.instance.poster = user_profile
        
        return super().form_valid(form)

class DeleteImageView(UserDetailsMixin, AssociatedTripMixin, DeleteView):
    '''deletion page for images'''
    model = Image
    template_name = "project/delete_image.html"
    context_object_name = "image"
    
class CreateProfileView(CreateView):
    '''view to create a new profile and user for the app'''
    form_class = CreateProfileForm
    template_name = "project/create_profile.html"
    
    def get_context_data(self, **kwargs):
        '''define context variables
            - also includes definition of a UserCreationForm
            '''
        context = super().get_context_data(**kwargs)
        user_creation_form = UserCreationForm(self.request.POST)
        print(f'user_creation_form: {user_creation_form}')
        
        context['UserCreationForm'] = user_creation_form
        
        return context

    def form_valid(self, form):
        '''process successful submission of the profile creation form'''
        userform = UserCreationForm(self.request.POST)
        
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
        '''redirect URL after form submission'''
        return reverse('show_all_trips')    
        
