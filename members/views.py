from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from members.forms import LoginForm, RegistrationForm
# Create your views here.

def register_view(request):
    # User already signed in redirected to homepage
    if request.user.is_authenticated:
        return redirect(reverse('posts:post_list'))

    # User submited the form
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('posts:post_list'))
        else:
            return render(request, 'members/register.html', {'form': form})
    
    # User access the endpoint via get request to complete the form 
    else:
        form = RegistrationForm()
        return render(request, 'members/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('posts:post_list'))
   
    # User submited the form
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('posts:post_list'))
        # Bad credentials, resend the form
        else:
            form = LoginForm(request.POST)
            return render(request, 'members/login.html', {'form': form})

    # User access the endpoint via get request to complete the form 
    else:
        form = LoginForm()
        return render(request, 'members/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(reverse('posts:post_list'))
