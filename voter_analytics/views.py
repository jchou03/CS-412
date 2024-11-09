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

    def get_queryset(self):
        '''limit the set of voter records being displayed'''
        voters = super().get_queryset().order_by("first_name")
        # sort through criteria
        for param in self.request.GET:
            value = self.request.GET[param]
            if value != "":
                if param=='party':
                    voters = voters.filter(party=value)
                elif param=='min_birth':
                    voters = voters.filter(birth_date__gte=f'{value}-01-01')
                elif param=='max_birth':
                    voters = voters.filter(birth_date__lte=f'{value}-12-31')
                elif param=='voter_score':
                    voters = voters.filter(voter_score=value)
                elif param=='v20state':
                    voters = voters.filter(v20state=(value == "on"))
                elif param=='v21town':
                    voters = voters.filter(v21town=(value=="on"))
                elif param=='v21primary':
                    voters = voters.filter(v21town=(value=="on"))
                elif param=='v22general':
                    voters = voters.filter(v21town=(value=="on"))
                elif param=='v23town':
                    voters = voters.filter(v21town=(value=="on"))
        return voters
    
    def get_context_data(self, **kwargs):
        '''define context data for the view'''
        context = super().get_context_data(**kwargs)
        context['years'] = range(1924,2024)
        context['parties'] = ["D", "R", "CC", "L", "T", "O", "G", "J", "Q", "FF"]
        context['voter_scores'] = range(0, 6)
        context['elections'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        return context