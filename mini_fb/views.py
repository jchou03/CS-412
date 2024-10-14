from django.shortcuts import render
from . models import *
from django.views.generic import *
from . forms import *
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

class CreateStatusMessageView(CreateView):
    '''view to enable users to create new status messages'''
    form_class = CreateStatusMessageForm
    template_name="mini_fb/create_status_form.html"
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        '''build template of context data (dict of kv pairs)'''
        context = super().get_context_data(**kwargs)
        # get the profile with the same primary key
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # add profile to context variable
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''identify Profile object to attach to the StatusMessage'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # set the profile field of the StatusMessage
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        '''redirect URL after form submission'''
        return reverse('show_profile', kwargs=self.kwargs)
        