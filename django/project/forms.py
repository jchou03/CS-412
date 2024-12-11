# File: forms.py
# Author: Jared Chou (jchou@bu.edu) 11/19/2024
# Description: Define the different forms and behavior of such forms throughout the project app.
# These forms are mainly used to create and update objects, but some include custom parameters to 
# influence form validation and processing. 

from django import forms
from .models import *
from django.core.validators import MinValueValidator

class CreateTripForm(forms.ModelForm):
    '''form to create a trip in the database'''
    class Meta:
        '''associate this form with the Trip model'''
        model = Trip
        fields = ['name', 'destination', 'start_date', 'end_date']

class UpdateTripForm(forms.ModelForm):
    '''form to update an existing trip'''
    class Meta:
        '''associate this form with the Trip model'''
        model = Trip
        fields = ['name', 'destination', 'start_date', 'end_date']
        
class CreateCostForm(forms.ModelForm):
    '''form to create a new cost'''
    class Meta:
        '''associate this form with the Cost model'''
        model = Cost
        fields = ['item_name', 'item_price', 'paid_by']
        
    def __init__(self, *args, **kwargs):
        '''update required state of certain fields'''
        super().__init__(*args, **kwargs)
        
        # make the the 'paid_by' field of the form not required for form submission
        self.fields['paid_by'].required = False
        
        # set the 'item_price' field to a custom FloatField with validation that it is non-negative
        item_price_field = forms.FloatField(
            validators=[MinValueValidator(0.0)],  # ensures that the value is non-negative
            error_messages={'min_value': 'Value must be positive.'})  # custom error message
        self.fields['item_price'] = item_price_field
        
class UpdateCostForm(forms.ModelForm):
    '''form to update properties of a specific cost'''
    class Meta:
        '''associate this form with the cost model'''
        model = Cost
        fields = ['item_name', 'item_price', 'paid_by']
    
    # set the 'item_price' field to a custom FloatField with validation that it is non-negative
    item_price = forms.FloatField(
            validators=[MinValueValidator(0.0)],  # ensures that the value is non negative
            error_messages={'min_value': 'Value must be positive.'})  # custom error message
    
class AddAttendeeToTripForm(forms.ModelForm):
    '''form to add a new attendee to a trip'''
    class Meta:
        '''associate this form with the AttendTrip model'''
        model=AttendTrip
        fields = ['profile']
        
    def __init__(self, *args, **kwargs):
        '''update options for possible users to add to the trip'''
        
        # Attendee_options will be passed as a kwarg to the form based on the profiles that are not
        # already attending the trip. This kwarg is removed and saved to not interfere with
        # super().__init__ but is used to update the select field options if provided
        attendee_options = kwargs.pop('attendee_options', None)
        
        super().__init__(*args, **kwargs) # initialize form
            
        # if attendee_options were provided, use the previously saved attendee_options as the 
        # queryset of options for the 'profile' field
        if attendee_options != None:
            print(f"attendee options found with {attendee_options}")
            self.fields['profile'].queryset = attendee_options

    
class CreateImageForm(forms.ModelForm):
    '''form to create a new image'''
    class Meta:
        '''associate this form with the Image model'''
        model = Image
        fields = ['image']
        
class CreateProfileForm(forms.ModelForm):
    '''form to create a new profile'''
    class Meta:
        '''associate this form with the Profile model'''
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']