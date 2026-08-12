from rest_framework.permissions import BasePermission


class IsApplicant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCompanyUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.job.company.owner == request.user
