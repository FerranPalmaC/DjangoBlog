from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.

def signup(request):
    # User already signed in redirected to homepage
    if request.user.is_authenticated:
        return redirect(reverse('posts:post_list'))

    # User submited the form
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('posts:post_list'))
        else:
            return render(request, 'members/signup.html', {'form': form})
    # Fist time user access signup
    else:
        form = UserCreationForm()
        return render(request, 'members/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('posts:post_list'))
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('posts:post_list'))
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'members/login.html', {'form': form})

    else:
        form = AuthenticationForm()
        return render(request, 'members/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(reverse('posts:post_list'))