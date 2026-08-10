from django.urls import path
from .views import ListCreateCompanyView, DetailUpdateDeleteView

urlpatterns = [
    path("", ListCreateCompanyView.as_view(), name="list-create-company"),
    path("me/", DetailUpdateDeleteView.as_view(), name="profile-update-delete"),
]
