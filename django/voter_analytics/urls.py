# voter_analytics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.VoterRecordsView.as_view(), name="voters"),
]