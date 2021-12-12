from django.db import models
from django.conf import settings
from django.forms import widgets
from django.forms.widgets import Widget
from user_data.validators import validate_image
from django_extensions.db.fields import AutoSlugField

class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_owner', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=250, blank=False, null=False)
    image = models.ImageField(upload_to='posts', blank=True, null=True, validators=[validate_image])
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL)
    has_been_edited = models.BooleanField(default=False)
    date_of_edit = models.DateTimeField(blank=True, null=True)
    slug = AutoSlugField(populate_from=['owner', 'date'])

    def __str__(self):
        return self.body

class PostComments(models.Model):
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class Friends(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="current_user", on_delete=models.CASCADE)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    class Meta:
        verbose_name_plural = "Friends"

    def __str__(self):
        return f"Friends of {self.user.first_name} {self.user.last_name}"

