from django.urls import path
from .views import (
    CreateJobView,
    ListJobView,
    ShowChangeDeleteJobView,
    SaveJobView,
    ListSavedJobsView,
)

urlpatterns = [
    path("", ListJobView.as_view(), name="list-jobs"),
    path("create/", CreateJobView.as_view(), name="create-jobs"),
    path("<int:pk>/", ShowChangeDeleteJobView.as_view(), name="show-change-delete-job"),
    path("<int:pk>/save/", SaveJobView.as_view(), name="save-job"),
    path("saved/", ListSavedJobsView.as_view(), name="saved-jobs-list"),
]
