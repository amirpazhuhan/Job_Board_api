from django.urls import path
from .views import (
    ListCreateJobView,
    ShowChangeDeleteJobView,
    SaveJobView,
    ListSavedJobsView,
)

urlpatterns = [
    path("", ListCreateJobView.as_view(), name="create-retrieve-jobs"),
    path("<int:pk>/", ShowChangeDeleteJobView.as_view(), name="show-change-delete-job"),
    path("<int:pk>/save/", SaveJobView.as_view(), name="save-job"),
    path("saved/", ListSavedJobsView.as_view(), name="saved-jobs-list"),
]
