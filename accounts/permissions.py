from rest_framework import permissions
from .models import RoleEnum

class IsJobseeker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleEnum.JOBSEEKER.value

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleEnum.EMPLOYER.value