from django.contrib import admin

from user_interface.models import Friends, Post, PostComments

@admin.register(Friends)
class FriendsModelAdministration(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostModelADministration(admin.ModelAdmin):
    pass

@admin.register(PostComments)
class PostModelADministration(admin.ModelAdmin):
    pass