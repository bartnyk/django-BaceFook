from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from user_data.forms import LoginForm

@login_required(login_url='/account/login/')
def timeline(request):
    return render(request, 'social/timeline.html')