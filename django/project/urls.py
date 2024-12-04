# project/urls.py
# description: app specific URLS for the project application

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # show all trips
    path(r'', views.ShowAllTripsView.as_view(), name="show_all_trips"),
    
    # trip views
    path(r'trip/<int:pk>', views.ShowTripView.as_view(), name="show_trip"),
    path(r'create_trip', views.CreateTripView.as_view(), name="create_trip"),
    path(r'trip/<int:pk>/delete', views.DeleteTripView.as_view(), name="delete_trip"),
    path(r'trip/<int:pk>/update', views.UpdateTripView.as_view(), name="update_trip"),
    
    # cost views
    path(r'trip/<int:trip_pk>/create_cost', views.CreateCostView.as_view(), name="create_cost"),
    path(r'trip/<int:trip_pk>/delete_cost/<int:pk>', views.DeleteCostView.as_view(), name="delete_cost"),
    path(r'trip/<int:trip_pk>/update_cost/<int:pk>', views.UpdateCostView.as_view(), name="update_cost"),
    
    # attendee views
    path(r'trip/<int:trip_pk>/add_attendee', views.AddAttendeeToTripView.as_view(), name="add_attendee"),
    path(r'trip/<int:pk>/remove_attendees', views.RemoveAttendeesView.as_view(), name="remove_attendees"),
    path(r'trip/<int:trip_pk>/remove_attendee/<int:pk>', views.RemoveAttendeeView.as_view(), name="remove_attendee"),
    
    # image views
    path(r'trip/<int:trip_pk>/create_img', views.CreateImageView.as_view(), name="create_img"),
    path(r'trip/<int:trip_pk>/delete_image/<int:pk>', views.DeleteImageView.as_view(), name="delete_image"),

    # auth views
    path(r'login', auth_views.LoginView.as_view(template_name="project/login.html"), name="login"),
    path(r'logout', auth_views.LogoutView.as_view(template_name="project/logged_out.html"), name="logout"),
    path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    # path(r'profile', views.ShowProfileView.as_view(), name="show_profile")
]