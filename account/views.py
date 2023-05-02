from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm


def login_excluded(redirect_to):
    # This decorator kicks authenticated users out of a view
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


@login_excluded('article:index')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('article:index')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('article:index')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})