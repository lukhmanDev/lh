from django.urls import path
from .views import (
    CategoryDetailView,
    CategoryListCreateView,
    PostDetailView,
    PostListCreateView,
    PostViewIncrementView,
)

urlpatterns = [
    # Posts endpoints
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<str:lookup>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<str:lookup>/view/', PostViewIncrementView.as_view(), name='post-view-increment'),

    # Category endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    # Blogs alias endpoints
    path('blogs/', PostListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<str:lookup>/', PostDetailView.as_view(), name='blog-detail'),
]
