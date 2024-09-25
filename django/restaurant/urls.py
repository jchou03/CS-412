# quotes/urls.py
# description: app-specific URLs for the quotes application 

from django.urls import path
from django.conf import settings
from . import views

# create list of URLs for the app
urlpatterns = [
    path(r'', views.main, name="main"),
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirm', views.confirm, name="confirm")
]
