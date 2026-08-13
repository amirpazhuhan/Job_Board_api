from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializer import RegisterSerializer, ChangePasswordSerializer, UserSerializer

# Create your views here.

User = get_user_model()


@extend_schema_view(
    get=extend_schema(summary="Get my profile", tags=["Authentication"]),
    put=extend_schema(summary="Replace my profile", tags=["Authentication"]),
    patch=extend_schema(summary="Update my profile", tags=["Authentication"]),
)
class ProfileView(RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(summary="Register", tags=["Authentication"])
class RegisterView(CreateAPIView):
    """Create a user account."""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


@extend_schema(summary="Change my password", tags=["Authentication"])
class ChangePasswordView(UpdateAPIView):
    """Change the authenticated user's password."""

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
