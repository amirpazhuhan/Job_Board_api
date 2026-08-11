from django.urls import path
from .views import ListCreateJobView, ShowChangeDeleteJobView

urlpatterns = [
    path("", ListCreateJobView.as_view(), name="create-retrieve-jobs"),
    path("<int:pk>/", ShowChangeDeleteJobView.as_view(), name="show-change-delete-job"),
]
