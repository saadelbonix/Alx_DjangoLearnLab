from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Comment, Tag

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. django, python, tips)"
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'tags_input')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            existing = ", ".join(t.name for t in self.instance.tags.all())
            self.fields['tags_input'].initial = existing

    def save(self, author=None, commit=True):
        post = super().save(commit=False)
        if author is not None:
            post.author = author
        if commit:
            post.save()
            # handle tags
            tags_str = self.cleaned_data.get('tags_input', '')
            names = [t.strip() for t in tags_str.split(',') if t.strip()]
            tags = []
            for name in names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            post.tags.set(tags)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment…'})
        }
