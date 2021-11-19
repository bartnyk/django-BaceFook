from django.contrib import admin

from user_interface.models import Friends

@admin.register(Friends)
class FriendsModelAdministration(admin.ModelAdmin):
    pass