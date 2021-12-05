from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'user_data'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('details/', account_details, name='details'),
    path('confirm/', send_confirmation, name='confirm'),
    path('confirm/<uuid:uuid>/', check_confirmation, name='check'),
    path('settings/', account_settings, name="account_settings"),
    path('change_password/', change_password, name="change_password"),
    path('details/<str:slug>/', account_details, name='other_acc_details'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)