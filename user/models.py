from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    """Application user with contact and hometown details."""

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    hometown = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
