from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

# Create your models here.


class Application(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWING = "reviewing", "Reviewing"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="applications"
    )
    cover_letter = models.TextField()
    resume = models.FileField(upload_to="media/")
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["job", "user"], name="job__user__application_unique"
            )
        ]
