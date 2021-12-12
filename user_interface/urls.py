from django.urls import path
from .views import PostDetail, timeline, FriendsList, edit_post
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

app_name = "user_interface"

urlpatterns = [
    path("", timeline, name='timeline'),
    path("friends/", login_required(FriendsList.as_view()), name="friends"),
    path("search/", login_required(FriendsList.as_view()), name="search"),
    path("post/<str:slug>/", login_required(PostDetail.as_view()), name='post-details'),
    path("post/edit/<str:slug>/", edit_post, name='edit-post')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
