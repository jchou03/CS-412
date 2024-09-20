# quotes/urls.py
# description: app-specific URLs for the quotes application 

from django.urls import path
from django.conf import settings
from . import views

# create list of URLs for the app
urlpatterns = [
    path(r'', views.quote, name="quote"), # first URL of app; give name to path matching the name of the function
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about")
]
