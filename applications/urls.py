from django.urls import path
from .views import (
    ListApplicationsView,
    JobApplyView,
    ApplicationDetailView,
    MyApplicationDetailView,
)

urlpatterns = [
    path("", ListApplicationsView.as_view(), name="list-applications"),
    path("<int:pk>/apply/", JobApplyView.as_view(), name="job-apply"),
    path("<int:pk>/", ApplicationDetailView.as_view(), name="application-detail-view"),
    path(
        "my/<int:pk>/",
        MyApplicationDetailView.as_view(),
        name="my-application-detail-view",
    ),
]
