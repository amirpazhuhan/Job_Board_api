from rest_framework.permissions import BasePermission


class IsApplicant(BasePermission):
    """Allow access only to the user who submitted an application."""

    def has_permission(self, request, view):
        company = getattr(request.user, "company", None)
        return request.user.is_authenticated and company is None

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCompanyUser(BasePermission):
    """Allow access only to the owner of the application's company."""

    def has_object_permission(self, request, view, obj):
        return obj.job.company.owner == request.user
