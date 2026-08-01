from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import LoginUserForm, RegisterUserForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index_url')
    form = RegisterUserForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Вы успешно зарегистрировались!')
        return redirect('index_url')
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index_url')
    form = LoginUserForm(request, data=request.POST)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index_url')
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, 'Вы успешно вышли из аккаунта!')
    return redirect('index_url')


@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'profile_user': request.user})