# voter_analytics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.VoterRecordsView.as_view(), name="voters"),
    path(r'voter/<int:pk>', views.VoterRecordView.as_view(), name="voter"),
    path(r'graphs', views.VoterGraphsView.as_view(), name="graphs")
]