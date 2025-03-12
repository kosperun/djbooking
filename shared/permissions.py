from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from users.models import User


class IsPartner(BasePermission):
    """
    Allows access only to partner users.
    """

    def has_permission(self, request, view) -> bool:
        return request.user and hasattr(request.user, "is_partner") and request.user.is_partner


def check_staff_permissions(actor: User) -> None:
    if not actor.is_staff:
        raise PermissionDenied()


def check_partner_permissions(actor: User) -> None:
    if not actor.is_partner:
        raise PermissionDenied()
