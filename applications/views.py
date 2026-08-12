from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from .permission import IsCompanyUser, IsApplicant
from .models import Application
from .serializer import ApplicationCreateSerializer, ApplicationDetailSerializer
from jobs.models import Job

# Create your views here.


class ListApplicationsView(ListAPIView):

    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = getattr(self.request.user, "company", None)

        if company is None:
            return self.request.user.applications.all()
        else:
            return Application.objects.filter(job__company=self.request.user.company)


class JobApplyView(CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsApplicant]

    def perform_create(self, serializer):
        job = Job.objects.get(pk=self.kwargs["pk"])
        if Application.objects.filter(job=job, user=self.request.user).exists():

            raise serializers.ValidationError(
                {"detail": "You have already applied to this job."}
            )

        return serializer.save(
            job=job,
            user=self.request.user,
        )


class ApplicationDetailView(RetrieveUpdateAPIView):

    serializer_class = ApplicationDetailSerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        return Application.objects.filter(job__company=self.request.user.company)


class MyApplicationDetailView(RetrieveUpdateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsApplicant]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)
