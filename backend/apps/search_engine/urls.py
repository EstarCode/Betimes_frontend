"""
Search Engine URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_documents, name='search-documents'),
    path('suggestions/', views.search_suggestions, name='search-suggestions'),
]
