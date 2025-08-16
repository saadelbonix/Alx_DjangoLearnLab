from django.urls import path
from .views import (
    HomeView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    RegisterView, ProfileView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # Posts
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # Comments
    path('posts/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    # Auth extras
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
