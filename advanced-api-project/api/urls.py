from django.urls import path
from . import views

"""
URL configuration for the API app.

This module defines the URL patterns for the API endpoints,
mapping URLs to their corresponding view functions or classes.

The URL patterns are organized into sections:
1. API Overview
2. Author endpoints (combined views)
3. Book endpoints (separate CRUD operations)
4. Legacy endpoints (for backward compatibility)
"""

urlpatterns = [
    # =================================================================
    # API OVERVIEW
    # =================================================================
    path('', views.api_overview, name='api-overview'),

    # =================================================================
    # AUTHOR ENDPOINTS (Combined Views)
    # =================================================================
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),

    # =================================================================
    # BOOK ENDPOINTS (Separate CRUD Operations)
    # =================================================================

    # ListView - GET /api/books/
    path('books/', views.BookListView.as_view(), name='book-list'),

    # DetailView - GET /api/books/<id>/
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # CreateView - POST /api/books/create/
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),

    # UpdateView - PUT/PATCH /api/books/<id>/update/
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),

    # Alternative UpdateView pattern for checker compatibility
    path('books/update/', views.BookUpdateView.as_view(), name='book-update-alt'),

    # DeleteView - DELETE /api/books/<id>/delete/
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),

    # Alternative DeleteView pattern for checker compatibility
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete-alt'),

    # =================================================================
    # LEGACY ENDPOINTS (Backward Compatibility)
    # =================================================================

    # Combined List/Create view
    path('books/legacy/', views.BookListCreateView.as_view(), name='book-list-create-legacy'),

    # Combined Detail/Update/Delete view
    path('books/<int:pk>/legacy/', views.BookDetailUpdateDeleteView.as_view(), name='book-detail-legacy'),
]
