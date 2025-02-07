from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'blog'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_post_list'),
    path('<int:pk>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('create/', BlogPostCreateView.as_view(), name='blog_post_create'),
    path('<int:pk>/update/', BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_post_delete'),
]
