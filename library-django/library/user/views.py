from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'Welcome, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
        return render(request, 'users/login.html')
    else:
        return redirect('home')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/registration.html', {"form": form})
