from rest_framework import serializers
from .models import Application


class ApplicationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["job", "user", "status", "created_at"]


class ApplicationDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["job", "user", "created_at"]
