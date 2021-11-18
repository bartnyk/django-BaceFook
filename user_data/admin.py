from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileModelAdministration(admin.ModelAdmin):
    fields = ['user', 'account_confirmed', 'uuid']
