from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from django.db import IntegrityError

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import Job, SavedJob
from .serializer import JobSerializer
from .permission import IsAuthorizedToModify, IsOwner

# Create your views here.


class JobFilter(filters.FilterSet):
    """Filter job listings by location, type, and salary bounds."""

    min_salary_min = filters.NumberFilter(field_name="salary_min", lookup_expr="gte")
    max_salary_min = filters.NumberFilter(field_name="salary_min", lookup_expr="lte")
    min_salary_max = filters.NumberFilter(field_name="salary_max", lookup_expr="gte")
    max_salary_max = filters.NumberFilter(field_name="salary_max", lookup_expr="lte")

    class Meta:
        model = Job
        fields = ["location", "employment_type"]


@extend_schema_view(
    get=extend_schema(
        summary="List jobs",
        tags=["Jobs"],
        parameters=[
            OpenApiParameter(
                "search", str, description="Search title and description."
            ),
            OpenApiParameter(
                "ordering",
                str,
                description="salary_min or salary_max; prefix with - for descending.",
            ),
        ],
    ),
)
class ListJobView(ListAPIView):
    """List searchable job listings"""

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = JobFilter
    search_fields = ["title", "description", "company__name"]
    ordering_fields = ["salary_min", "salary_max"]


@extend_schema(
    summary="Create a job",
    description="Create a new job for the authenticated user's company.",
    tags=["Jobs"],
)
class CreateJobView(CreateAPIView):
    """create one job for the caller's company."""

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


@extend_schema_view(
    get=extend_schema(summary="Get a job", tags=["Jobs"]),
    put=extend_schema(summary="Replace a job", tags=["Jobs"]),
    patch=extend_schema(summary="Update a job", tags=["Jobs"]),
    delete=extend_schema(summary="Delete a job", tags=["Jobs"]),
)
class ShowChangeDeleteJobView(RetrieveUpdateDestroyAPIView):
    """Retrieve a job or let its owner update or delete it."""

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToModify]


@extend_schema_view(
    post=extend_schema(summary="Save a job", tags=["Saved jobs"]),
    delete=extend_schema(summary="Remove a saved job", tags=["Saved jobs"]),
)
class SaveJobView(APIView):
    """Add or remove a job from the caller's saved jobs."""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, pk):
        user = request.user
        job = get_object_or_404(Job, pk=pk)

        if SavedJob.objects.filter(user=user, job=job).exists():
            raise ValidationError({"detail": "This job is already saved."})

        try:
            SavedJob.objects.create(user=user, job=job)
        except IntegrityError:
            raise ValidationError({"detail": "This job is already saved."})
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        job = get_object_or_404(Job, pk=pk)

        saved_job = get_object_or_404(SavedJob, user=user, job=job)
        saved_job.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(summary="List saved jobs", tags=["Saved jobs"])
class ListSavedJobsView(ListAPIView):
    """List the job listings saved by the caller."""

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(saved_by__user=self.request.user)
