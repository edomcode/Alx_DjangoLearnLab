from django.urls import path
from . import views

"""
URL configuration for the API app.

This module defines the URL patterns for the API endpoints,
mapping URLs to their corresponding view functions or classes.
"""

urlpatterns = [
    # API overview endpoint
    path('', views.api_overview, name='api-overview'),
    
    # Author endpoints
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Book endpoints
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
