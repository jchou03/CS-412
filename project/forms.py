from django import forms
from .models import *

class CreateTripForm(forms.ModelForm):
    '''form to create a profile in the database'''
    class Meta:
        '''associate this form with the Profile model'''
        model = Trip
        fields = ['name', 'destination', 'start_date', 'end_date']