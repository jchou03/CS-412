from django.shortcuts import render
from django.views.generic import *
from .models import *

# Create your views here.
class VoterRecordsView(ListView):
    '''display a list of all voter records'''
    template_name="voter_analytics/voters.html"
    model=Voter
    context_object_name = 'voters'
    paginate_by = 100

    # def get_queryset(self):
    #     '''limit the set of voter records being displayed'''
    #     voters = super().get_queryset().order_by("first_name")
    #     return voters[:100]        
    
    