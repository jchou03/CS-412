from django.shortcuts import render
from django.views.generic import *
from . models import *

# Create your views here.
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
    