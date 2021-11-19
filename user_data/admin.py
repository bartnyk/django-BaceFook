from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileModelAdministration(admin.ModelAdmin):
    list_display = ('user_name', 'uuid', 'account_confirmed')

    def user_name(self, v):
        return v.user.first_name + " " + v.user.last_name