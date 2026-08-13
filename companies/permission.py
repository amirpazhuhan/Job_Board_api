from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        company = getattr(request.user, "company", None)
        return company is not None
