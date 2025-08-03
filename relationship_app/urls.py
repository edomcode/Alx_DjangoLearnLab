from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('authors/', views.authors_list, name='authors'),
    path('books/', views.book_list, name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
]
