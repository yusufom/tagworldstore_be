from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(("Email"), max_length=500)
    phone = models.CharField(max_length=20)
