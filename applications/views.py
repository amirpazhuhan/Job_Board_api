from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .permission import IsCompanyUser, IsApplicant
from .models import Application
from .serializer import ApplicationCreateSerializer, ApplicationDetailSerializer
from jobs.models import Job

# Create your views here.


@extend_schema(summary="List applications", tags=["Applications"])
class ListApplicationsView(ListAPIView):
    """List the caller's applications or applications for their company jobs."""

    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = getattr(self.request.user, "company", None)

        if company is None:
            return self.request.user.applications.all()
        else:
            return Application.objects.filter(job__company=self.request.user.company)


@extend_schema(summary="Apply to a job", tags=["Applications"])
class JobApplyView(CreateAPIView):
    """Create an application for the job identified by the URL."""

    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsApplicant]

    def perform_create(self, serializer):
        job = get_object_or_404(Job, pk=self.kwargs["pk"])

        if not job.is_active:
            raise serializers.ValidationError(
                {"detail": "You cannot apply to an inactive job."}
            )

        if Application.objects.filter(job=job, user=self.request.user).exists():

            raise serializers.ValidationError(
                {"detail": "You have already applied to this job."}
            )

        try:
            serializer.save(
                job=job,
                user=self.request.user,
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "You have already applied to this job."}
            )


@extend_schema_view(
    get=extend_schema(summary="Get a company application", tags=["Applications"]),
    put=extend_schema(summary="Replace an application status", tags=["Applications"]),
    patch=extend_schema(summary="Update an application status", tags=["Applications"]),
)
class ApplicationDetailView(RetrieveUpdateAPIView):
    """Let a company owner review and update an application."""

    serializer_class = ApplicationDetailSerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        return Application.objects.filter(job__company=self.request.user.company)


@extend_schema_view(
    get=extend_schema(summary="Get my application", tags=["Applications"]),
    put=extend_schema(summary="Replace my application", tags=["Applications"]),
    patch=extend_schema(summary="Update my application", tags=["Applications"]),
)
class MyApplicationDetailView(RetrieveUpdateAPIView):
    """Let an applicant retrieve or update their own application."""

    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsApplicant]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)
