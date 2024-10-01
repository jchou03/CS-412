# blog/urls.py
# description: app specific URLS for blog application

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name="show_all")
]