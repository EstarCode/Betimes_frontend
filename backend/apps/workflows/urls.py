"""
URL configuration for workflows
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkflowTemplateViewSet, WorkflowInstanceViewSet

router = DefaultRouter()
router.register(r'templates', WorkflowTemplateViewSet, basename='workflow-template')
router.register(r'instances', WorkflowInstanceViewSet, basename='workflow-instance')

urlpatterns = [
    path('', include(router.urls)),
]
