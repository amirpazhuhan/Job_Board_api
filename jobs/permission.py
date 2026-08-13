from rest_framework.permissions import BasePermission


class IsAuthorizedToModify(BasePermission):
    """Allow only the listing's company owner to modify it."""

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT", "DELETE"]:
            company = getattr(request.user, "company", None)
            return obj.company == company

        return True


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        company = getattr(request.user, "company", None)
        return company is not None
