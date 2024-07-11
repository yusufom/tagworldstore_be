from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, 
    PermissionsMixin, Group
)
import random


# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, phone, password=None):

        if email is None:
            raise TypeError('Users must have an email address')
        
        if first_name is None:
            raise TypeError('First Name is required')
        
        if last_name is None:
            raise TypeError('Last Name is required')

        if phone is None:
            raise TypeError("User must have a phone number")

        user = self.model(first_name=first_name, last_name=last_name, email=self.normalize_email(email), phone=phone)
        user.set_password(password)
        user.username = generate_uniquie_username()
        user.save()

        return user

    def create_superuser(self, first_name, last_name, phone, email,  password):
        if first_name is None:
            raise TypeError('Users must have a Firstname')

        if email is None:
            raise TypeError('Users must have an email address')

        if phone is None:
            raise TypeError("User must have a phone number")

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone,  password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, verbose_name='ID')
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    username = models.CharField(db_index=True, max_length=255, unique=True)
    phone = models.CharField(max_length=13, unique=True, default=0)
    
    objects = UserManager()
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']



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
        Profile.objects.create(user=instance, email=instance.email, first_name=instance.first_name, last_name=instance.last_name, phone=instance.phone)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
@receiver(post_delete, sender=User)
def pre_delete(sender, instance, **kwargs):
    try:
        profile = Profile.objects.get(user=instance)
        profile.delete()
    except Profile.DoesNotExist:
        pass
    
    
def generate():
    
    ten_digits = str(random.randint(1000000000, 9999999999))
    return ten_digits
    
def generate_uniquie_username():
    # Generates a unique username id
    unique_username = generate()
    
    # Filter user by the generated unique username id
    user = User.objects.filter(username=unique_username)

    """
    Checks if a user with the generated unique username id does not exist,
    then go ahead and set the unique username to the incoming user
    """
    if not user:
        username = unique_username
        return username