from django import forms
from .models import *

class CreateTripForm(forms.ModelForm):
    '''form to create a profile in the database'''
    class Meta:
        '''associate this form with the Profile model'''
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

class AddAttendeeToTripForm(forms.ModelForm):
    '''form to add a new attendee to a trip'''
    class Meta:
        '''associate this form with the AttendTrip model'''
        model=AttendTrip
        fields = ['profile']
        
    # def __init__(self, *args, **kwargs):
    #     '''update options for possible users to add'''