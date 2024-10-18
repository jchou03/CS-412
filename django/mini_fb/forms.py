from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    '''form to create a profile in the database'''
    class Meta:
        '''associate this form with the Profile model'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
        
class CreateStatusMessageForm(forms.ModelForm):
    '''form to create a status message for a given profile'''
    class Meta:
        '''associate this form with the StatusMessage model'''    
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    '''form to update a profile afeter it has been created'''
    class Meta:
        '''associate this form with the Profile model'''
        model = Profile
        fields = ['city', 'email', 'profile_image_url']