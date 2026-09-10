from django.urls import path
from .api_views import JobListCreateAPI

urlpatterns = [
    path('jobs/', JobListCreateAPI.as_view(), name='api_jobs'),
]