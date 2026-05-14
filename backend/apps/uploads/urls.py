"""
URL configuration for chunked uploads
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChunkedUploadViewSet

router = DefaultRouter()
router.register(r'uploads', ChunkedUploadViewSet, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
]
