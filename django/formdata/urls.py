# formdata/urls.py
# description: app-specific URLs for the hw application 

from django.urls import path
from django.conf import settings
from . import views

# create list of URLs for the app
urlpatterns = [
    path(r'', views.show_form, name="show_form"),
    path(r'submit', views.submit, name="submit"),
]
