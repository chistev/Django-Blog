from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='password_reset'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_complete'),
]
