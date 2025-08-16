from django.urls import path
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),

    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/new/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),

    path("posts/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:pk>/edit/", views.CommentUpdateView.as_view(), name="comment_update"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),

    path("search/", views.SearchView.as_view(), name="search"),
    path("tags/<str:tag_name>/", views.TagView.as_view(), name="tag_posts"),
]
