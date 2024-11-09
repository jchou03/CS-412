from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Result
import plotly
import plotly.graph_objs as go

# Create your views here.
class ResultListView(ListView):
    '''view to display marathon results'''
    
    template_name = 'marathon_analytics/results.html'
    model=Result
    context_object_name = "results"
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
    
class ResultDetailView(DetailView):
    '''show detail about a single page'''
    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'
    
    def get_context_data(self, **kwargs):
        '''provide context data variables'''
        # start with superclass information
        context = super().get_context_data(**kwargs)
        r = context['r']
        
        # create graph of first/second half pie chart
        x = ['first half', 'second half']
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second
        y = [first_half_seconds, second_half_seconds]
        
        # generate pie chart
        fig = go.Pie(labels=x, values = y)
        title_text = f"Half Marathon Splits"
        
        # obtain graph as html div
        graph_div_splits = plotly.offline.plot({
            "data": [fig],
            "layout_title_text": title_text,
        }, auto_open=False,output_type="div")
        
        context['graph_div_splits'] = graph_div_splits
        
        # generate graph of runners that this runner passed/got passed by
        x = [f'Runners passed by {r.first_name}', f'Runners who passed {r.first_name}']
        y = [r.get_runners_passed(), r.get_runners_passed_by()]
        fig = go.Bar(x=x, y=y)
        title_text=f'Runners passed/passed by'
        graph_div_passed = plotly.offline.plot({
            "data": [fig],
            "layout_title_text": title_text
        }, auto_open=False, output_type="div")
        
        context['graph_div_passed'] = graph_div_passed
        
        return context