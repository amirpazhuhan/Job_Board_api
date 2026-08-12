from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import Job, SavedJob
from .serializer import JobSerializer
from .permission import IsAuthorizedToModify

# Create your views here.


class ListCreateJobView(ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class ShowChangeDeleteJobView(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToModify]


class SaveJobView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, pk):
        user = request.user
        job = get_object_or_404(Job, pk=pk)

        if SavedJob.objects.filter(user=user, job=job).exists():
            raise ValidationError({"detail": "This job is already saved."})
        SavedJob.objects.create(user=user, job=job)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        job = get_object_or_404(Job, pk=pk)

        saved_job = get_object_or_404(SavedJob, user=user, job=job)
        saved_job.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSavedJobsView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(saved_by__user=self.request.user)
