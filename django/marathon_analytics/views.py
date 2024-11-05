from django.shortcuts import render
from django.views.generic import ListView
from .models import Result

# Create your views here.
class ResultListView(ListView):
    '''view to display marathon results'''
    
    template_name = 'marathon_analytics/results.html'
    model=Result
    context_object_name = "results"
    
    def get_queryset(self):
        '''limit results; return the set of Results'''
        # use superclass to get the queryset
        template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50
    def get_queryset(self):
        # start with entire queryset
        qs = super().get_queryset().order_by('place_overall')
        # filter results by these field(s):
        if 'first_name' in self.request.GET:
            first_name = self.request.GET['first_name']
            if first_name:
                # case insensitive with __icontains
                qs = qs.filter(first_name__icontains=first_name)
                
        return qs