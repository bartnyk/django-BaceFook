from django.core import mail
from django.http.request import validate_host
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, resolve
from .models import Profile
from django.core.mail import send_mail
from json import load
from django.core.exceptions import ObjectDoesNotExist
from os.path import dirname, join, abspath


def login_view(request): 
    if request.user.is_authenticated:
        return redirect(reverse('user_interface:timeline'))   
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username_or_mail'], password=cd['password'])
            print(user)
            if user is not None:
                print('hehe')
                login(request, user)
                if user.last_login is None:
                    return redirect(reverse('user_data:confirm'))
                return redirect(reverse("user_interface:timeline"))
    else:
        form = LoginForm()
    return render(request, "authentication/login.html", {"form": form})

@login_required(login_url='user_data:login')
def logout_view(request):
    logout(request)
    return render(request, 'authentication/logout.html')

def registration_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('user_interface:timeline'))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd['username'],
                first_name=cd['first_name'],
                last_name = cd['last_name'],
                email=cd['email'],
                password=cd['password'],
                active=True
            )
            return redirect(reverse("user_data:login"), {"purpose": "first_login"})
    else:
        form = RegisterForm()
    return render(request, 'authentication/registration.html', {"form": form})

@login_required(login_url="user_data:login")
def account_details(request):
    if not Profile.objects.get(user=request.user).account_confirmed:
        return render(request, 'authentication/registration_confirmation.html', {'mail': request.user.email, 'purpose': 'resend'})
    return render(request, 'social/account.html')

@login_required(login_url='user_data:login')
def send_confirmation(request): 
    user = request.user
    profile = Profile.objects.get(user=user)
    if profile.account_confirmed:
        return redirect(reverse("user_interface:timeline"))
    with open(join(dirname(abspath(__file__)), 'mail_bodies.json'), 'r') as mail_data:
        data = load(mail_data)['confirmation']
    subject = user.first_name + " " + user.last_name + f" | {data[0]}"
    to = user.email
    uuid = profile.uuid
    body = data[1] + request.build_absolute_uri(f"/account/confirm/{uuid}")
    send_mail(
        subject=subject,
        message=body,
        recipient_list=[to],
        fail_silently=False,
        from_email='contact@somedoma.in'
    )
    return render(request, 'authentication/registration_confirmation.html', {'mail': to, 'purpose': 'first'})

def check_confirmation(request, uuid):
    context = {}
    try:
        obj = Profile.objects.get(uuid=uuid)
        obj.account_confirmed = True
        obj.save()
        context["result"] = "Success!"
    except ObjectDoesNotExist:
        context['result'] = "Something goes wrong."
        logout(request)
    return render(request, 'authentication/check_result.html', context)
    
    


