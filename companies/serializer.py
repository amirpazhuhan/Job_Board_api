from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """Serialize company profiles while keeping ownership server-managed."""

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "logo",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context["request"]

        if self.instance is None and getattr(request.user, "company", None) is not None:
            raise serializers.ValidationError({"detail": "You already have a company."})

        return attrs
