from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_owner', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL)

class PostComments(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)

# class Likes(models.Model):
#     post = models.OneToOneField(Post, on_delete=models.CASCADE)
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Friends(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="current_user", on_delete=models.CASCADE)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name_plural = "Friends"

    def __str__(self):
        return f"Friends of {self.user.first_name} {self.user.last_name}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_friends_modes(sender, instance=None, created=False, **kwargs):
    if created:
        Friends.objects.create(user=instance)