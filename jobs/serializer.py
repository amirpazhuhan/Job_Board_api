from rest_framework import serializers
from .models import Job, SavedJob


class JobSerializer(serializers.ModelSerializer):
    """Serialize job listings and validate their salary range."""

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["id", "company", "created_at", "updated_at", "is_active"]

    def validate(self, attrs):
        salary_min = attrs.get(
            "salary_min",
            getattr(self.instance, "salary_min", None),
        )
        salary_max = attrs.get(
            "salary_max",
            getattr(self.instance, "salary_max", None),
        )

        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                raise serializers.ValidationError(
                    "Maximum salary cannot be lower than minimum salary."
                )

        return attrs
