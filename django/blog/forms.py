# blog/forms.py

from django import forms
from .models import *

class CreateArticleForm(forms.ModelForm):
    '''a form to create a new Article'''
    class Meta:
        '''associate this form with a model, specifically which fields to create'''
        model = Article
        fields = ['author', 'title', 'text', 'image_file']
    
    