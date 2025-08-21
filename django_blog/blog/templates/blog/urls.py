from django.urls import path
from . import views

urlpatterns = [
   
    path("search/", views.search_posts, name="search_posts"),
    path("tags/<str:tag_name>/", views.posts_by_tag, name="posts_by_tag"),
]
