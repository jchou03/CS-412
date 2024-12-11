# File: mixins.py
# Author: Jared Chou (jchou@bu.edu) 12/5/2024
# Description: Define custom Mixin objects that are incorporated into the different views of the app
# to consistently define common/shared behaviors

from . models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib.parse import urlencode
from django.shortcuts import redirect

def encode_url(url_name, obj):
    '''Encode a url with a context object.
    This function is used to encode a url when parameters want to be stored in request.GET for
    reference by other views
    '''
    base_url = reverse(url_name)
    query_str = urlencode(obj)
    url = '{}?{}'.format(base_url, query_str)
    return url

def get_trip_pk(kwargs):
    '''Return either pk or trip_pk depending on state of kwargs. 
    
    Depending on the view, some views will have a kwarg of 'pk' refer to the pk of the specified trip
    while other views will have a pk refer to an object of a different model with a kwarg of 'trip_pk'
    to refer to the pk of the associated trip. 
    
    This function is used to ensure the correct trip pk is used when processing kwargs
    '''
    
    pk = 1
    if 'trip_pk' in kwargs:
        pk = kwargs['trip_pk']
    else:
        pk = kwargs['pk']    
    
    return pk

# custom mixins for views
class UserDetailsMixin(object):
    '''class to share sign in details'''    
    def get_user_profile(self, user):
        '''get a profile from a user'''
        return Profile.objects.filter(user=user).first()
    
    def get_context_data(self, **kwargs):
        '''update the context data to include'''
        context = super().get_context_data(**kwargs) # get other context variables from superclass
        if self.request.user.is_authenticated:
            # find profile associated with the logged in user
            profile = self.get_user_profile(self.request.user)
            # save this profile object to the context for reference in templates
            context['logged_in_profile'] = profile
        else: 
            # if the user is not authenticated, set the 'logged_in_profile' context variable to None
            context['logged_in_profile'] = None

        return context
    
class AssociatedTripMixin():
    '''Mixin to represent shared behavior for views that require relationships to a specific trip.
    For example, after a new cost is created, we want to redirect the user to the trip that the created 
    cost is associated with.
    '''
    def get_context_data(self, **kwargs):
        '''add primary key of the associated trip'''
        context = super().get_context_data(**kwargs) # get other context variables from superclass
        
        # Parse the kwargs of this view to find the value of the 'trip_pk' kwarg for reference in the 
        # html templates. This is used so pages that want to reference back to a specific trip have
        # access to the trip's primary key.
        context['trip_pk'] = self.kwargs['trip_pk']
        return context
    
    def get_success_url(self):
        '''redirect url to the trip that the newly created object is attached to'''
        return reverse('show_trip', kwargs={"pk":self.kwargs["trip_pk"]})
    
class AttendeeRequiredTripMixin(UserDetailsMixin, LoginRequiredMixin):
    '''Mixin that prevents users from accessing trip modification pages unless they are authenticated
    and an attendee of that trip.
    '''
    
    def profile_attends_trip(self, trip, profile):
        '''helper function to check if the provided profile is an attendee of the trip'''
        return profile in trip.get_attendees()
    
    def dispatch(self, request, *args, **kwargs):
        '''Data processing when a user tries to access a restricted page to ensure that the user 
        is a trip attendee before displaying the data.
        '''
        
        # get the trip object of the trip associated with this view (as determined by get_trip_pk)
        trip_pk = get_trip_pk(self.kwargs) 
        trip = Trip.objects.get(pk=trip_pk)
        profile = None # define the profile variable to check if the user is an attendee
        
        # update profile variable if the user is currently logged in
        if request.user.is_authenticated:
            profile = self.get_user_profile(self.request.user)

        # Check if the user is not authenticated or not an attendee. 
        # If so, process the no_permission page
        if (not request.user.is_authenticated) or (not self.profile_attends_trip(trip, profile)):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        '''page to display no permissions'''
        
        # get the associated trip's primary key based on kwargs
        trip_pk = get_trip_pk(self.kwargs)
        
        # define the object that defines that request.GET.next variable used to redirect the user
        # from the 'no_access' view. Then redirect the user to the 'no_access' view.
        obj = {'next': reverse('join_trip', kwargs={'pk': trip_pk})}
        return redirect(encode_url('no_access', obj))
