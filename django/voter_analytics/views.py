from django.shortcuts import render
from django.views.generic import *
from .models import *
import plotly
import plotly.graph_objs as go

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
    
class VoterRecordView(DetailView):
    '''display the record of a single voter'''
    model=Voter
    template_name="voter_analytics/voter.html"
    context_object_name="voter"
    
    def get_context_data(self, **kwargs):
        '''get context data for template'''
        context = super().get_context_data(**kwargs)
        context['fields'] = Voter._meta.fields
        print(context['fields'])
        return context
    
class VoterGraphsView(ListView):
    '''display graphs about aggregate voter data'''
    
    model=Voter
    template_name="voter_analytics/graphs.html"

    def get_context_data(self, **kwargs):
        '''generate graphs and add to context data'''
        context = super().get_context_data(**kwargs)
        
        # count number of voters for each year
        years = []
        party_counts = {}
        election_participation = []
        for v in Voter.objects.all():
            # count birth years
            years.append(v.birth_date.year)
            # count parties
            if v.party in party_counts:
                party_counts[v.party] += 1
            else:
                party_counts[v.party] = 1
            # count election participation
            elections = ["v20state", 'v21town', 'v21primary', 'v22general', 'v23town']
            for e in elections:
                if getattr(v, e):
                    election_participation.append(e)
        
        # fig = go.Histogram(x=years)
        # title_text = f"Voters by Birth Year"
        # graph_voter_birth_years = plotly.offline.plot({"data":[fig], "layout_title_text": title_text}, auto_open=False, output_type="div")
        # context['voter_birth_years'] = graph_voter_birth_years

        # distribution of voters by party
        # fig = go.Pie(values=list(party_counts.values()), labels=list(party_counts.keys()))
        # title_text = f"Voters by Party"
        # graph_voter_parties = plotly.offline.plot({"data":[fig], "layout_title_text": title_text}, auto_open=False, output_type="div")
        # context['voter_parties'] = graph_voter_parties
        
        # distribution of voter participation across elections
        fig = go.Histogram(x=election_participation)
        title_text = f"Voters by Election"
        graph_election_participation = plotly.offline.plot({"data":[fig], "layout_title_text": title_text}, auto_open=False, output_type="div")
        context['election_participation'] = graph_election_participation
        
        return context