from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Friends
from user_data.forms import LoginForm

@login_required(login_url='/account/login/')
def timeline(request):
    return render(request, 'social/timeline.html')


class FriendsList(generic.ListView):
    paginate_by = 50
    template_name = 'social/friends_list.html'
    login_url = "/account/login/"
    context_object_name = 'friends_list'

    def get_queryset(self):
        return Friends.objects.get(user=self.request.user).friends.all()
