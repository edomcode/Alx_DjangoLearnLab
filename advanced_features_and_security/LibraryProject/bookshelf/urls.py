from django.urls import path
from . import views  

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('books/', views.view_books, name='view_books'),
    path('add/', views.create_book, name='create_book'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('example-form/', views.example_form_view, name='example_form'),
    
]