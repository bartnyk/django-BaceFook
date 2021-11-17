from django.urls import path
from .views import timeline

app_name = "user_interface"

urlpatterns = [
    path("", timeline, name='timeline')
]