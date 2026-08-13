from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Company(models.Model):
    """Company profile owned by one authenticated user."""

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company",
    )

    name = models.CharField(max_length=250, blank=False)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="media/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
