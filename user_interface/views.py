from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import request
from django.http.response import HttpResponseRedirect
from django.views import generic
from .models import Friends, Post, PostComments
from .forms import CreateComment, CreatePost
from django.db.models import Q, query
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

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

def post_like(post, action, user):
    if action == "like":
        post.likes.add(user)
    elif action == "dislike":
        post.likes.remove(user)

@login_required
def timeline(request):
    if not request.user.profile.account_confirmed:
        return render(request, 'authentication/registration_confirmation.html', {'mail': request.user.email, 'purpose': 'resend'})
    friends = Friends.objects.get(user = request.user).friends.all()
    posts = [Post.objects.filter(owner=friend).order_by('-date') for friend in friends]
    if request.method == "POST":
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                owner = request.user,
                body = form.cleaned_data['body'],
                image = request.FILES.get('image'),
            )
            return redirect(reverse("user_interface:timeline"))
    else:
        form = CreatePost()
    return render(request, 'social/timeline.html', {"form": form, "posts_obj": posts})


class FriendsList(generic.ListView):
    # paginate_by = 50
    template_name = 'social/friends_list.html'
    login_url = "/accounts/login/"
    context_object_name = 'list'

    def get_queryset(self):
        if self.request.GET.get('q'):
            q = User.objects.all()
            for term in self.request.GET.get('q').split(" "):
                q = q.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
        else:
            q = Friends.objects.get(user=self.request.user).friends.all().exclude(username=self.request.user.username)
        return q

    def post(self, *a, **k):
        usr = User.objects.get(username=self.request.POST.get('usr'))
        Friends.objects.get(user=self.request.user).friends.remove(usr)
        if self.request.POST.get('btn') == "Delete friend": remove_friend(usr, self.request.user)            
        elif self.request.POST.get('btn') == "Add friend": add_friend(usr, self.request.user)
        elif self.request.POST.get('btn') == "Message": pass
        return HttpResponseRedirect(self.request.get_full_path_info())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.profile.account_confirmed:
            self.template_name = 'authentication/registration_confirmation.html'
            context['mail'] = self.request.user.email
            context['purpose'] =  "resend"
        else:
            context['friends'] = Friends.objects.get(user=self.request.user).friends.all()
        return context
    
class PostDetail(generic.DetailView):
    slug_field = 'slug'
    model = Post
    template_name = 'social/post_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comments'] = PostComments
        context['form'] = CreateComment()
        return context

    def post(self, *a, **kw):
        cd = self.request.POST
        post_obj = Post.objects.get(id=cd['post_id'])
        print(cd)
        if self.request.POST.get('like'):
            post_like(post_obj, cd['like'], self.request.user)
        else:
            PostComments.objects.create(
                owner = self.request.user,
                post = post_obj,
                comment = cd['comment']
            )
        return HttpResponseRedirect(self.request.get_full_path_info()) 

def edit_post(request, slug):
    post = Post.objects.get(slug=slug)
    if not post.owner == request.user:
        return redirect(reverse("user_interface:timeline"))
    else:
        form = CreatePost(request.POST, request.FILES)
        if request.method == "POST":
            if request.POST.get('delete'): 
                post.delete()
                return redirect(reverse('user_interface:timeline'))
            if form.is_valid():
                cd = form.cleaned_data
                if request.POST.get('image-clear') == 'on': post.image = None
                if cd['image'] != "": post.image = request.FILES.get('image')
                post.body = cd['body']
                post.has_been_edited = True
                post.date_of_edit = timezone.now()
                post.save()
                return redirect(f'/post/{slug}')
        form = CreatePost(initial={"body": post.body, "image": post.image})
    return render(request, 'social/post_edit.html', {'form': form})