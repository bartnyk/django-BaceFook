from django.urls import path
from .views import login_view, logout_view, account_details, registration_view, send_confirmation, check_confirmation

app_name = 'user_data'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('details/', account_details, name='details'),
    path('confirm/', send_confirmation, name='confirm'),
    path('confirm/<uuid:uuid>/', check_confirmation, name='check'),
]
