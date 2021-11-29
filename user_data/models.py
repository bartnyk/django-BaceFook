from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import uuid
from user_interface.models import Friends

MALES = (
    ('None', ''),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
    
)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images', default='images/default.png')
    date_of_birth = models.DateField(blank=True, null=True)
    male = models.CharField(max_length=30, choices=MALES, default='None')
    about = models.TextField(blank=True, null=True)
    account_confirmed = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created: 
        Profile.objects.create(user=instance)
        Friends.objects.create(user=instance, friends=instance)
