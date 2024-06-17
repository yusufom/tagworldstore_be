from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField

# Create your models here.

class Slide(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 720x724")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.title, self.subtitle)