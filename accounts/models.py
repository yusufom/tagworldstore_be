from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(("Email"), max_length=500)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    profile = Profile.objects.get(user=instance, email=instance.email)
    profile.delete()