from django.http.request import validate_host
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


def login_view(request): 
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_interface:timeline'))   
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username_or_mail'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("user_interface:timeline")
    else:
        form = LoginForm()
    return render(request, "authentication/login.html", {"form": form})

@login_required(login_url='user_data:login')
def logout_view(request):
    logout(request)
    return render(request, 'authentication/logout.html')


def registration_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_interface:timeline'))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(email=cd['email']).exists():
                raise ValidationError("User with this email address already exists.")
            elif User.objects.filter(username=cd['username']).exists():
                raise ValidationError("User with this login already exists.")
            else:
                del(cd['password2'])
                User.objects.create(
                    username=cd['username'],
                    first_name=cd['first_name'],
                    last_name = cd['last_name'],
                    email=cd['email'],
                    password=cd['password']
                )
                return render(request, 'authentication/registration_success.html', {'mail': cd['email']})
    else:
        form = RegisterForm()
    return render(request, 'authentication/registration.html', {"form": form})
