from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
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
from user_interface.models import Post, Friends
from user_interface.views import add_friend, remove_friend
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

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

@login_required
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
                last_name=cd['last_name'],
                email=cd['email'],
                password=cd['password'],
                )
            Profile.objects.get(user=user).male=cd['male']
            request.session['email'] = cd['email']
            return redirect(reverse("user_data:login"))
    else:
        form = RegisterForm()
    return render(request, 'authentication/registration.html', {"form": form})

@login_required
def account_details(request, slug=None):
    friends_obj = Friends.objects.get(user=request.user)
    context = {}
    if slug is None:
        if not request.user.profile.account_confirmed:
            return render(request, 'authentication/registration_confirmation.html', {'mail': request.user.email, 'purpose': 'resend'})
        profile = Profile.objects.get(user=request.user)
        context['owner'] = True
    else:
        profile = get_object_or_404(Profile, slug=slug)
        if profile == Profile.objects.get(user=request.user):
            context['owner'] = True
        if profile.user in friends_obj.friends.all():
            context['is_friend'] = True

    if request.method == "POST":        
        btn = request.POST['btn']
        if btn == "Add friend": 
            add_friend(profile.user, request.user)
        elif btn == "Delete friend":
            remove_friend(profile.user, request.user)
        elif btn == "Account settings": return redirect(reverse('user_data:account_settings'))
        elif btn == "Message": pass # Not ready yet
        return HttpResponseRedirect(request.path_info)

    context['profile'] = profile
    context['posts'] = Post.objects.filter(owner=profile.user).order_by('-date')
    return render(request, 'social/account.html', context)

@login_required
def send_confirmation(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if profile.account_confirmed:
        return redirect(reverse("user_interface:timeline"))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mail_bodies.json'), 'r') as mail_data:
        data = load(mail_data)['confirmation']
    subject = user.first_name + " " + user.last_name + f" | {data[0]}"
    to = user.email
    uuid = profile.uuid
    body = data[1] + request.build_absolute_uri(f"/accounts/confirm/{uuid}")
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
    
@login_required
def account_settings(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        form = AdditionalInfoForm(request.POST, request.FILES)
        if form.is_valid() and request.POST.get('confirm'):
            cd = form.cleaned_data
            print(cd)
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            profile.date_of_birth = cd['date_of_birth']
            profile.male = cd['male']
            profile.about = cd['about']
            img = request.FILES.get("image")
            if img is not None:
                profile.profile_picture = img
            user.save()
            profile.save()
            return redirect(reverse('user_data:details'))
        else:
            action = request.POST.get('btn')
            if action == 'Change password': return redirect(reverse('user_data:password_change'))
            elif action == 'Change e-mail address': return redirect(reverse('user_data:change_email'))
            elif action == 'Change username': return redirect(reverse('user_data:change_username'))
            elif action == 'Delete account': return redirect(reverse('user_data:delete_account'))
    else:
        form = AdditionalInfoForm(initial={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": profile.date_of_birth,
            "male": profile.male,
            "about": profile.about
        })
    return render(request, 'social/settings.html', {"form": form})

@login_required
def change_email_or_username(request):
    action = request.path.split("/")[-2]
    u = request.user
    if request.method == "POST":
        if action == 'email':
            form = ChangeEmail(request.user, request.POST)
        elif action == 'username':
            form = ChangeUsername(request.user, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd.get('username'): u.username = cd.get('username')
            elif cd.get('email'): u.email = cd.get('email')
            u.save()
            return redirect(reverse('user_data:details'))
    else:        
        if action == 'email':
            form = ChangeEmail(request.user)
        elif action == 'username':
            form = ChangeUsername(request.user)
    return render(request, 'authentication/change.html', {'form': form})

def delete_account(request):
    usr = request.user
    if request.method == "POST":
        form = TypePassword(request.user, request.POST)
        print(form.errors)
        if form.is_valid(): 
            usr.delete()
            return redirect(reverse("user_data:login"))
    else:
        form = TypePassword(request.user)
    return render(request, 'authentication/delete_account.html', {"form": form})
            