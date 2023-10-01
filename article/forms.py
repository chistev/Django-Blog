from django import forms
from .models import Post  # Import the Post model from your models.py


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'category', 'post']