from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

import logging 
logger1 = logging.getLogger('file')
logger = logging.getLogger('file2')

def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:recommend')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }

    return render(request, 'accounts_form.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:index')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts_form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

def mypage(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'mypage.html', context)

def mypage_main(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'mypage_main.html', context)

def bookmark_list(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'bookmark_list.html', context)

