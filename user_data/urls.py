from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView

app_name = 'user_data'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
    path('register/', registration_view, name='register'),
    path('change_password/', PasswordChangeView.as_view(template_name='authentication/password_change.html', success_url="success/"), name='password_change'),
    path('change_password/success/', PasswordChangeDoneView.as_view(template_name='authentication/password_change_success.html'), name='password_change_done'),
    path('profile/', account_details, name='details'),
    path('confirm/', send_confirmation, name='confirm'),
    path('confirm/<uuid:uuid>/', check_confirmation, name='check'),
    path('settings/', account_settings, name="account_settings"),
    path('details/<str:slug>/', account_details, name='other_acc_details'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)