# mini_fb/urls.py
# description: app specific URLS for mini_fb application

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all"),
    path(r'home', views.ShowAllProfilesView.as_view(), name="show_all")
]