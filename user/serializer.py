from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, password_changed

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

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
    """
    Validate and update the authenticated user's password.

    The serializer requires the user's current password and a new password.
    It verifies that the current password is correct, validates the new
    password against Django's configured password validators, and updates
    the user's password if all validation succeeds.
    """

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
        """
        Ensure the supplied current password matches the user's
        existing password.

        This method is called automatically by DRF during
        ``serializer.is_valid()``.
        """
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("The current password is incorrect.")

        return value

    def validate_new_password(self, value):
        """
        Validate the proposed new password.

        Django's password validation framework checks requirements
        such as minimum length, similarity to user information,
        common passwords, and numeric-only passwords (depending on
        project settings).
        """
        validate_password(value)
        return value

    def save(self):
        """
        Replace the authenticated user's password.

        This method should be called only after successful validation.
        The serializer updates the user's password using Django's
        ``set_password()`` method, which securely hashes the password
        before saving it to the database.

        After the password is changed, Django's password validators
        are notified through ``password_changed()``.
        """
        # The instance is supplied by UpdateAPIView via get_object().
        user = self.instance

        # Retrieve the validated new password.
        password = self.validated_data["new_password"]

        # Hash the password and assign it to the user.
        user.set_password(password)

        # Persist the updated password hash.
        user.save()

        # Notify Django's password validation framework that the
        # password has been successfully changed.
        password_changed(password, user)

        return user
