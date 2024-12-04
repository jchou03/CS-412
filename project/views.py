from django.shortcuts import render, redirect
from django.views.generic import *
from . models import *
from . forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.base import ContextMixin

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
    
class CreateTripView(CreateView):
    '''view to create a new trip'''
    form_class = CreateTripForm
    template_name = "project/create_trip.html"
        
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
    
class AddAttendeeToTripView(AssociatedTripMixin, CreateView):
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
        
