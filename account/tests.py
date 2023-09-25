from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from .forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    def test_valid_registration(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'securepass123',
            'password2': 'securepass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, User)

    def test_missing_required_fields(self):
        form_data = {}  # Missing all required fields
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_invalid_email_format(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'securepass123',
            'password2': 'securepass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'securepass123',
            'password2': 'differentpass',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_unique_username(self):
        User.objects.create_user(username='testuser', password='securepass123')
        form_data = {
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
