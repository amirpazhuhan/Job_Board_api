from django.db import models
from companies.models import Company
from django.contrib.auth import get_user_model

# Create your models here.


class Job(models.Model):
    """A job listing published by a company."""

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    location = models.CharField(max_length=255, blank=True)
    employment_type = models.CharField(max_length=255, blank=True)
    salary_min = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    salary_max = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SavedJob(models.Model):
    """A user's bookmarked job listing."""

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="saved_jobs"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "job"], name="unique_SavedJobs")
        ]
