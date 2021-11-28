from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Profile
from django.core.mail import send_mail
from json import load
from django.core.exceptions import ObjectDoesNotExist
import os


def login_view(request): 
    if request.user.is_authenticated:
        return redirect(reverse('user_interface:timeline'))   
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username_or_mail'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse("user_data:confirm"))
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
            User.objects.create_user(
                username=cd['username'],
                first_name=cd['first_name'],
                last_name = cd['last_name'],
                email=cd['email'],
                password=cd['password'],
                )
            request.session['email'] = cd['email']
            return redirect(reverse("user_data:login"))
    else:
        form = RegisterForm()
    return render(request, 'authentication/registration.html', {"form": form})

@login_required(login_url="user_data:login")
def account_details(request):
    if not Profile.objects.get(user=request.user).account_confirmed:
        return render(request, 'authentication/registration_confirmation.html', {'mail': request.user.email, 'purpose': 'resend'})
    profile = Profile.objects.get(user=request.user)
    return render(request, 'social/account.html', {"profile": profile})

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
        obj.user is request.user
        obj.account_confirmed = True
        obj.save()
        context["result"] = "Success!"
    except ObjectDoesNotExist:
        context['result'] = "Something goes wrong."
        logout(request)
    return render(request, 'authentication/check_result.html', context)
    
@login_required(login_url='user_data:login')
def account_settings(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        form = AdditionalInfoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            profile.date_of_birth = cd['date_of_birth']
            profile.about = cd['about']
            print(request.FILES.get("profile_pic"))
            if request.FILES.get("profile_pic") is not None:
                profile.profile_picture = request.FILES.get("profile_pic")
            user.save()
            profile.save()
            return redirect(reverse('user_data:details'))
    else:
        form = AdditionalInfoForm(initial={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": profile.date_of_birth,
            "about": profile.about
        })
    return render(request, 'social/settings.html', {"form": form})

def change_password(request):
    form = PasswordChange
    if request.method == "POST":
        if form.is_valid():
            pass
    return render(request, 'authentication/password_change.html', {'form': form})
