# quotes/urls.py
# description: app-specific URLs for the quotes application 

from django.urls import path
from django.conf import settings
from . import views

# create list of URLs for the app
urlpatterns = [
    path(r'', views.main, name="main"), # first URL of app; give name to path matching the name of the function
]