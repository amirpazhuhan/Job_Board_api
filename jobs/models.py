from django.db import models
from companies.models import Company

# Create your models here.


class Job(models.Model):

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    location = models.CharField(max_length=255, blank=True)
    employment_type = models.CharField(max_length=255, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
