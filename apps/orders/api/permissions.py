from rest_framework.permissions import BasePermission


class GuestPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == request.user.ROLE_GUEST


class OwnerPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == request.user.ROLE_OWNER
