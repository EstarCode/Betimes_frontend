"""
URL configuration for conversion.
"""

from django.urls import path
from .views import ConversionUploadView, ConversionJobListView, ConversionJobDetailView

app_name = 'conversion'

urlpatterns = [
    path('', ConversionUploadView.as_view(), name='upload'),
    path('jobs/', ConversionJobListView.as_view(), name='job_list'),
    path('jobs/<uuid:id>/', ConversionJobDetailView.as_view(), name='job_detail'),
]
