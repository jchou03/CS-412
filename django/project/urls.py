# project/urls.py
# description: app specific URLS for the project application

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'', views.ShowAllTripsView.as_view(), name="show_all_trips"),
    path(r'trip/<int:pk>', views.ShowTripView.as_view(), name="show_trip"),
    path(r'create_trip', views.CreateTripView.as_view(), name="create_trip"),
    path(r'create_cost/<int:pk>', views.CreateCostView.as_view(), name="create_cost"),
    path(r'add_attendee/<int:pk>', views.AddAttendeeToTripView.as_view(), name="add_attendee"),
    path(r'create_img/<int:pk>', views.CreateImageView.as_view(), name="create_img"),
    path(r'login', auth_views.LoginView.as_view(template_name="project/login.html"), name="login"),
    path(r'logout', auth_views.LogoutView.as_view(template_name="project/logged_out.html"), name="logout"),
]