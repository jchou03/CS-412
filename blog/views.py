# blog/views.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from django.views.generic import ListView

# Create your views here.
class ShowAllView(ListView):
    '''a view to show all articles'''
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"
    
    