from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.views import generic
from .models import Friends, Post
from .forms import CreatePost
from django.db.models import Q
from django.shortcuts import render

def add_friend(u1, u2): #pass obj's
    f1 = Friends.objects.get(user=u1)
    f2 = Friends.objects.get(user=u2)
    f1.friends.add(u2)
    f2.friends.add(u1)

def remove_friend(u1, u2):
    f1 = Friends.objects.get(user=u1)
    f2 = Friends.objects.get(user=u2)
    f1.friends.remove(u2)
    f2.friends.remove(u1)

@login_required(login_url='/account/login/')
def timeline(request):
    friends = Friends.objects.get(user = request.user).friends.all()
    posts = [Post.objects.filter(owner=friend).order_by('-date') for friend in friends]
    if request.method == "POST":
        form = CreatePost(request.POST)
        if form.is_valid():
            Post.objects.create(
                owner = request.user,
                body = form.cleaned_data['body'],
                image = request.FILES.get('image'),
            )
            form = CreatePost
    else:
        form = CreatePost()
    return render(request, 'social/timeline.html', {"form": form, "posts_obj": posts})


class FriendsList(generic.ListView):
    # paginate_by = 50
    template_name = 'social/friends_list.html'
    login_url = "/account/login/"
    context_object_name = 'list'

    def get_queryset(self):
        if self.request.GET.get('q') is not None:
            q = User.objects.all()
            for term in self.request.GET.get('q'):
                q = q.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
        else:
            q = Friends.objects.get(user=self.request.user).friends.all().exclude(username=self.request.user.username)
        return q

    def post(self, *a, **k):
        if self.request.POST.get('btn') == "Delete friend": #friends_obj.friends.remove(profile.user)
            usr = User.objects.get(username=self.request.POST.get('usr'))
            Friends.objects.get(user=self.request.user).friends.remove(usr)
            remove_friend(usr, self.request.user)
        elif self.request.POST.get('btn') == "Message": pass
        print(self.request.POST)
        return HttpResponseRedirect(self.request.path_info)

