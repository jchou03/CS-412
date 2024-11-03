from django.shortcuts import render
from . models import *
from django.views.generic import *
from . forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class MiniFBLoginRequiredMixin(LoginRequiredMixin):
    '''a mixin that defines the same redirect behavior for a LoginRequiredMixin'''
    def get_login_url(self):
        '''redirect url if a user is not signed in'''
        return "login"

class SignedInUserDetails():
    '''class to share sign in details'''
    
    def get_user_profile(self, user):
        '''get a profile from a user'''
        return Profile.objects.filter(user=user).first()
    
    def get_context_data(self, **kwargs):
        '''update the context data to include'''
        # find user who is logged in
        print(f'request:{self.request.user}')
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            # find profile 
            # add to context data
            profile = self.get_user_profile(self.request.user)
            context['logged_in_profile'] = profile

        return context
    
    def get_object(self):
        '''get the associated profile for this view'''
        return self.get_user_profile(self.request.user)   

class ShowAllProfilesView(SignedInUserDetails, ListView):
    '''a view to show all profiles'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"
    
class ShowProfilePageView(SignedInUserDetails, DetailView):
    '''view to show a single profile (with a larger profile picture)'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"
    
    
    def get_object(self):
        '''override SignedInUserDetails implementation with the DetailView'''
        return DetailView.get_object(self)
        
    
class CreateProfileView(SignedInUserDetails, CreateView):
    '''view to enable users to create new profiles from UI
    
    on GET: send back from
    on POST: read form data, create an instance of a Profile, and save to database'''
    
    form_class = CreateProfileForm
    template_name="mini_fb/create_profile_form.html"
    
    def get_context_data(self, **kwargs):
        '''add the user creation form to the context data variable'''
        context = super().get_context_data(**kwargs)
        form = UserCreationForm(self.request.POST)
        print(f'form: {form}')
        print(f'form isvalid: {form.is_valid()}')

        context['UserCreationForm'] = form
    
        return context
    
    def form_valid(self, form):
        '''create a new user and profile'''
        print(f'profile creation was valid with inputs {self.request.POST}')
        userform = UserCreationForm(self.request.POST)
        
        if not userform.is_valid():
            # validate the userform and return response if there are errors
            return self.render_to_response(self.get_context_data(form=form, UserCreationForm=userform))
            
        user = userform.save()
        form.instance.user = user
        # print(f'registered user: {user}')
        login(self.request, user)

        return super().form_valid(form)
        

class CreateStatusMessageView(MiniFBLoginRequiredMixin, SignedInUserDetails, CreateView):
    '''view to enable users to create new status messages'''
    form_class = CreateStatusMessageForm
    template_name="mini_fb/create_status_form.html"
    
    def form_valid(self, form):
        '''identify Profile object to attach to the StatusMessage'''
        profile = Profile.objects.filter(user=self.request.user).first()
        # set the profile field of the StatusMessage
        form.instance.profile = profile
        
        # saving the new status message
        sm = form.save()
        # read the uploaded file(s) from the form
        files = self.request.FILES.getlist('files')
        
        for f in files:
            image = Image()
            image.image = f
            image.statusMessage = sm
            image.save()
        
        return super().form_valid(form)

    def get_success_url(self):
        '''redirect URL after form submission'''
        kwargs = self.kwargs
        kwargs['pk'] = self.get_user_profile(self.request.user).pk
        return reverse('show_profile', kwargs=self.kwargs)

class UpdateProfileView(MiniFBLoginRequiredMixin, SignedInUserDetails, UpdateView):
    '''view to update an existing profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    context_object_name = "profile"
    
    def get_object(self):
        '''get the associated profile for this update view'''
        return self.get_user_profile(self.request.user)

class DeleteStatusMessageView(MiniFBLoginRequiredMixin, SignedInUserDetails, DeleteView):
    '''view to delete an existing status message'''
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status"
    
    def get_success_url(self):
        '''redirect URL after successful deletion'''
        self.kwargs['pk'] = self.get_context_data()['object'].profile.pk
        return reverse('show_profile', kwargs=self.kwargs)
        
class UpdateStatusMessageView(MiniFBLoginRequiredMixin, SignedInUserDetails, UpdateView):
    '''view to update an existing status message'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = "status"
    
    def get_success_url(self):
        '''redirect URL after successful update'''
        self.kwargs['pk'] = self.get_context_data()['object'].profile.pk
        return reverse('show_profile', kwargs = self.kwargs)
    
class CreateFriendView(MiniFBLoginRequiredMixin, SignedInUserDetails, View):
    '''view to add a friendship between two profiles'''
    def dispatch(self, request, *args, **kwargs):
        print(self.kwargs)
        p1 = self.get_user_profile(self.request.user)
        p2 = Profile.objects.get(pk=self.kwargs["other_pk"])
        p1.add_friend(p2)
        
        return redirect('show_profile', pk=p1.pk)

class ShowFriendSuggestionsView(SignedInUserDetails, DetailView):
    '''view to display friend suggestions for a profile'''
    model=Profile
    template_name="mini_fb/friend_suggestions.html"
    context_object_name="profile"
    
class ShowNewsFeedView(MiniFBLoginRequiredMixin, SignedInUserDetails, DetailView):
    '''view to display the news feed'''
    model = Profile
    template_name="mini_fb/news_feed.html"
    context_object_name="profile"