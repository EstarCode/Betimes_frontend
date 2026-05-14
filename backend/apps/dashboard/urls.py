"""
URL configuration for dashboard
"""
from django.urls import path
from .views import DashboardMetricsView, UploadStatisticsView, StorageUsageView

urlpatterns = [
    path('metrics/', DashboardMetricsView.as_view(), name='dashboard-metrics'),
    path('uploads/', UploadStatisticsView.as_view(), name='upload-statistics'),
    path('storage/', StorageUsageView.as_view(), name='storage-usage'),
]
