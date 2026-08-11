from rest_framework.permissions import BasePermission


class IsAuthorizedToModify(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT", "DELETE"]:
            return obj.company == request.user.company

        return True
