"""
URL configuration for compression.
"""

from django.urls import path
from .views import (
    CompressionUploadView,
    CompressionJobListView,
    CompressionJobDetailView,
    CompressionJobDeleteView
)

app_name = 'compression'

urlpatterns = [
    path('', CompressionUploadView.as_view(), name='upload'),
    path('jobs/', CompressionJobListView.as_view(), name='job_list'),
    path('jobs/<uuid:id>/', CompressionJobDetailView.as_view(), name='job_detail'),
    path('jobs/<uuid:id>/delete/', CompressionJobDeleteView.as_view(), name='job_delete'),
]
