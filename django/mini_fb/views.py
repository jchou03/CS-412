from django.shortcuts import render
from . models import *
from django.views.generic import *

# Create your views here.
class ShowAllProfilesView(ListView):
    '''a view to show all profiles'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"
    
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"
    
