from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import UserLoginForm, UserRegistrationForm, ProfileEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import User


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Вы вошли в аккаунт')
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return redirect(request.POST.get('next'))
                return redirect(reverse('posts:home'))

    form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def user_logout(request):
    messages.success(request, 'Вы вышли из аккаунта')
    logout(request)
    return redirect(reverse('posts:home'))


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            login(request, user)
            messages.success(request, f'{user.username}, Вы успешно зарегистрированы ')
            return redirect(reverse('users:edit'))

    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/registration.html', context)


@login_required
def user_profile(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username)
    else:
        profile = request.user
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль отредактирован')
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def profile_delete(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Аккаунт удвлен')
        return redirect('posts:home')
    return render(request, 'users/profile_delete.html')
