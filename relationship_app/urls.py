from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('authors/', views.authors_list, name='authors'),
]
