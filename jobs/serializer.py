from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["id", "company", "created_at", "updated_at", "is_active"]

    def validate(self, attrs):
        salary_min = attrs.get("salary_min")
        salary_max = attrs.get("salary_max")
        if salary_min > salary_max:
            raise serializers.ValidationError(
                "Maximum salary can not be lower than minimum salary."
            )
        return attrs
