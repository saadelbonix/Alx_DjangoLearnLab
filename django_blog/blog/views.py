from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
)
from django.db.models import Q

from .models import Post, Comment, Tag
from .forms import RegisterForm, ProfileForm, PostForm, CommentForm

# Home / List with search and optional tag filter
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('author').prefetch_related('tags')
        q = self.request.GET.get('q')
        tag = self.request.GET.get('tag')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()
        if tag:
            qs = qs.filter(tags__name__iexact=tag).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        ctx['active_tag'] = self.request.GET.get('tag')
        ctx['all_tags'] = Tag.objects.all()
        return ctx

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.save(author=self.request.user)
        messages.success(self.request, "Post created successfully.")
        return redirect(self.object.get_absolute_url() if getattr(self, 'object', None) else 'home')

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.save(author=self.request.user)
        messages.success(self.request, "Post updated successfully.")
        return redirect(self.object.get_absolute_url())

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted.")
        return super().delete(request, *args, **kwargs)

# Comments
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        messages.success(self.request, "Comment added.")
        return redirect(post.get_absolute_url())

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Comment updated.")
        return redirect(self.object.post.get_absolute_url())

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        messages.success(self.request, "Comment deleted.")
        return self.object.post.get_absolute_url()

# Auth: register & profile
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        user.email = form.cleaned_data['email']
        user.save()
        login(self.request, user)
        messages.success(self.request, "Welcome! Your account was created.")
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Profile updated.")
        return super().form_valid(form)
