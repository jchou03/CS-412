from django.shortcuts import render, redirect
from django.views.generic import *
from . models import *
from . forms import *

# Create your views here.
class SignedInUserDetails():
    '''class to share sign in details'''
    
    def get_user_profile(self, user):
        '''get a profile from a user'''
        return Profile.objects.filter(user=user).first()
    
    def get_context_data(self, **kwargs):
        '''update the context data to include'''
        # find user who is logged in
        print(f'request:{self.request.user}')
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            # find profile 
            # add to context data
            profile = self.get_user_profile(self.request.user)
            context['logged_in_profile'] = profile

        return context
    
    def get_object(self):
        '''get the associated profile for this view'''
        return self.get_user_profile(self.request.user)   

class ShowAllTripsView(ListView):
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
    
class ShowTripView(DetailView):
    '''a view that displays a single trip'''
    model = Trip
    context_object_name = "trip"
    template_name = "project/show_trip.html"
    
class CreateTripView(CreateView):
    '''view to create a new trip'''
    form_class = CreateTripForm
    template_name = "project/create_trip.html"
    
    # def form_valid(self, form):
    #     '''create a new trip based on the valid form submission'''
        
class CreateCostView(CreateView):
    '''view to create a new cost'''
    form_class = CreateCostForm
    template_name = "project/create_cost.html"
    
    def get_context_data(self, **kwargs):
        '''add context variables'''
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context
    
    def form_valid(self, form):
        '''create a new cost based on a valid form submission'''
        if (form.instance.paid_by == None):
            # if paid by is empty, this is a planned cost, not an actual cost
            form.instance.actual_cost = False
        else:
            form.instance.actual_cost = True
            
        # get the trip
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        form.instance.trip = trip
        
        return super().form_valid(form)
        
    def get_success_url(self):
        '''redirect URL after form submission'''
        return reverse('show_trip', kwargs=self.kwargs)
    
class AddAttendeeToTripView(CreateView):
    '''view to add a new attendee to a trip'''
    form_class = AddAttendeeToTripForm
    template_name = 'project/add_attendee_to_trip.html'
    
    def get_context_data(self, **kwargs):
        '''add context variables'''
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context
    
    def form_valid(self, form):
        '''process form upon submission'''
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        form.instance.trip = trip    
        
        # check that this profile hasn't been added to the trip already
        attendees = trip.get_attendees()
        if form.instance.profile in attendees:
            print(f'the profie {form.instance.profile} is already attending the trip {trip}')
            return redirect('show_trip', pk=trip.pk)
        else:
            return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('show_trip', kwargs=self.kwargs)
    
class CreateImageView(CreateView):
    '''view to create a new image'''
    form_class = CreateImageForm
    template_name = "project/create_image.html"
    
    def get_context_data(self, **kwargs):
        '''add context variables'''
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context
    
    # def form_valid(self, form):
    #     '''process successful form submission'''
    #     # get the user 
    