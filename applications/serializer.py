from rest_framework import serializers
from .models import Application


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serialize applications submitted by job seekers."""

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["job", "user", "status", "created_at"]


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """Serialize applications and permit company status updates."""

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["job", "user", "cover_letter", "resume", "created_at"]
