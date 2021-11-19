from django.urls import path
from .views import timeline, FriendsList
from django.conf.urls.static import static
from django.conf import settings

app_name = "user_interface"

urlpatterns = [
    path("", timeline, name='timeline'),
    path("friends/", FriendsList.as_view(), name="friends"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
