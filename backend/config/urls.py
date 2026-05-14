"""
URL configuration for PDF Utility SaaS Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.dashboard.health import health_check, readiness_check, liveness_check

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Betimes Enterprise API",
        default_version='v1',
        description="Production-grade enterprise document processing platform API",
        terms_of_service="https://www.betimes.com/terms/",
        contact=openapi.Contact(email="support@betimes.com"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Health checks
    path('health/', health_check, name='health'),
    path('health/ready/', readiness_check, name='readiness'),
    path('health/live/', liveness_check, name='liveness'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API v1 Endpoints
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.uploads.urls')),  # Chunked uploads
    path('api/v1/', include('apps.versions.urls')),  # Document version control
    path('api/v1/workflows/', include('apps.workflows.urls')),  # Enterprise workflows
    path('api/v1/dashboard/', include('apps.dashboard.urls')),  # Dashboard metrics
    path('api/v1/compress/', include('apps.compression.urls')),  # PDF compression
    path('api/v1/convert/', include('apps.conversion.urls')),  # Document conversion
    path('api/v1/tools/pdf/', include('apps.pdf_tools.urls')),  # PDF tools (split/merge)
    path('api/v1/search/', include('apps.search_engine.urls')),  # Global search
    path('api/v1/analytics/', include('apps.analytics.urls')),  # Analytics
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
