from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView

from .serializer import RegisterSerializer, ChangePasswordSerializer, UserSerializer

# Create your views here.

User = get_user_model()


class ProfileView(RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_class = [AllowAny]
    serializer_class = RegisterSerializer


class ChangePasswordView(UpdateAPIView):

    permission_class = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
