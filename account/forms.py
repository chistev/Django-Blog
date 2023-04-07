from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# to create a custom registration field


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
