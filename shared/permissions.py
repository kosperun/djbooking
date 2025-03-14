from rest_framework.permissions import BasePermission


class IsPartner(BasePermission):
    """
    Allows access only to partner users.
    """

    def has_permission(self, request, view) -> bool:
        return request.user and hasattr(request.user, "is_partner") and request.user.is_partner


class IsStaffUser(BasePermission):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        return request.user and hasattr(request.user, "is_staff") and request.user.is_staff
