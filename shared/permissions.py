from rest_framework.permissions import BasePermission


class IsPartner(BasePermission):
    """
    Allows access only to partner users.
    """

    def has_permission(self, request, view) -> bool:
        return request.user and hasattr(request.user, "is_partner") and request.user.is_partner
