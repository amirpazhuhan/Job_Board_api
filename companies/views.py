from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializer import CompanySerializer
from .models import Company
from .permission import IsOwner

# Create your views here.


@extend_schema_view(
    get=extend_schema(summary="List companies", tags=["Companies"]),
    post=extend_schema(summary="Create my company", tags=["Companies"]),
)
class ListCreateCompanyView(ListCreateAPIView):
    """List companies or create the caller's company profile."""

    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema_view(
    get=extend_schema(summary="Get my company", tags=["Companies"]),
    put=extend_schema(summary="Replace my company", tags=["Companies"]),
    patch=extend_schema(summary="Update my company", tags=["Companies"]),
    delete=extend_schema(summary="Delete my company", tags=["Companies"]),
)
class DetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete the caller's company profile."""

    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user.company
