# hw/urls.py
# description: app-specific URLs for the hw application 

from django.urls import path
from django.conf import settings
from . import views

# create list of URLs for the app
urlpatterns = [
    path(r'', views.home, name="home"), # first URL of app; give name to path matching the name of the function
]
