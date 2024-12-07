from django import forms
from .models import *

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
        self.fields['paid_by'].required = False
        
class UpdateCostForm(forms.ModelForm):
    '''form to update properties of a specific cost'''
    class Meta:
        '''associate this form with the cost model'''
        model = Cost
        fields = ['item_name', 'item_price', 'paid_by']

class AddAttendeeToTripForm(forms.ModelForm):
    '''form to add a new attendee to a trip'''
    class Meta:
        '''associate this form with the AttendTrip model'''
        model=AttendTrip
        fields = ['profile']
        
    def __init__(self, *args, **kwargs):
        '''update options for possible users to add to the trip'''
        attendee_options = kwargs.pop('attendee_options', None)
        
        super().__init__(*args, **kwargs)
            
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