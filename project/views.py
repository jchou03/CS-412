from django.shortcuts import render
from django.views.generic import *
from . models import *

# Create your views here.
class ShowAllTripsView(ListView):
    '''view that displays all trips'''
    model = Trip
    context_object_name = "trips"
    template_name = "project/show_all_trips.html"
    
class ShowTripView(DetailView):
    '''a view that displays a single trip'''
    model = Trip
    context_object_name = "trip"
    template_name = "project/show_trip.html"
    