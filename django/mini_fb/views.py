from django.shortcuts import render
from . models import *
from django.views.generic import *
from . forms import CreateProfileForm
from django.urls import reverse

# Create your views here.
class ShowAllProfilesView(ListView):
    '''a view to show all profiles'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"
    
class ShowProfilePageView(DetailView):
    '''view to show a single profile (with a larger profile picture)'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"
    
class CreateProfileView(CreateView):
    '''view to enable users to create new profiles from UI
    
    on GET: send back from
    on POST: read form data, create an instance of a Profile, and save to database'''
    
    form_class = CreateProfileForm
    template_name="mini_fb/create_profile_form.html"
    