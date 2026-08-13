from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, password_changed

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serialize the editable profile fields of an authenticated user."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "hometown",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """Validate registration data and create a user with a hashed password."""

    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "hometown",
        )

    def validate_password(self, value):

        validate_password(value)
        return value

    def create(self, validated_data):

        password = validated_data.pop("password")
        user = User.objects.create_user(
            password=password,
            **validated_data,
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Validate the current password and persist a valid replacement."""

    old_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
        help_text="The user's current password.",
    )

    new_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
        help_text=(
            "The new password. It must satisfy Django's configured "
            "password validation rules."
        ),
    )

    def validate_old_password(self, value):
        """Ensure the current password matches the authenticated user."""
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("The current password is incorrect.")

        return value

    def validate_new_password(self, value):
        """Validate the replacement with Django's password validators."""
        validate_password(value)
        return value

    def save(self):
        """Hash, save, and notify validators about the new password."""
        user = self.instance
        password = self.validated_data["new_password"]
        user.set_password(password)
        user.save()
        password_changed(password, user)

        return user
