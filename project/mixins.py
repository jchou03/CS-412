from . models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib.parse import urlencode
from django.shortcuts import redirect

def encode_url(url_name, obj):
    '''encode a url with a context object'''
    base_url = reverse(url_name)
    query_str = urlencode(obj)
    url = '{}?{}'.format(base_url, query_str)
    return url

def get_trip_pk(kwargs):
    '''return either pk or trip_pk depending on state of kwargs. 
    This is used to ensure the correct trip pk is used when both a related trip pk and 
    object pk are in a single view'''
    
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
        # find user who is logged in
        # print(f'request:{self.request.user}')
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # find profile 
            # add to context data
            profile = self.get_user_profile(self.request.user)
            context['logged_in_profile'] = profile
        else: 
            context['logged_in_profile'] = None

        return context
    
class AssociatedTripMixin():
    '''mixin to represent shared behavior for views that require relationships to a specific trip'''
    def get_context_data(self, **kwargs):
        '''add primary key of the associated trip'''
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        return context
    
    def get_success_url(self):
        '''redirect url to the trip that the newly created object is attached to'''
        return reverse('show_trip', kwargs={"pk":self.kwargs["trip_pk"]})
    
class AttendeeRequiredTripMixin(UserDetailsMixin, LoginRequiredMixin):
    '''mixin that prevents users from accessing trip modification pages unless they are an attendee of that trip'''
    
    def profile_attends_trip(self, trip, profile):
        '''helper function to check if the provided profile is an attendee of the trip'''
        return profile in trip.get_attendees()
    
    def dispatch(self, request, *args, **kwargs):
        '''extra processing to ensure that the user is a trip attendee'''
        trip_pk = get_trip_pk(self.kwargs)
        trip = Trip.objects.get(pk=trip_pk)
        profile = None
        
        if request.user.is_authenticated:
            profile = self.get_user_profile(self.request.user)

        if (not request.user.is_authenticated) or (not self.profile_attends_trip(trip, profile)):
            return self.handle_no_permission()
        
        print(f'request: {request}')
        
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        '''page to display no permissions'''
        
        trip_pk = get_trip_pk(self.kwargs)
        
        obj = {'next': reverse('join_trip', kwargs={'pk': trip_pk})}
        return redirect(encode_url('no_access', obj))
