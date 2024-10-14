from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    '''form to create a profile in the database'''
    class Meta:
        '''associate this form with the Profile model'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
        
        