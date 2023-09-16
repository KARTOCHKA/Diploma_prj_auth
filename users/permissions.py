from rest_framework import permissions

from users.models import User


class IsVerifiedUser(permissions.BasePermission):
    """
    Check if the user has permission to access the requested view.

    Parameters:
        request (object): The HTTP request object.
        view (object): The requested view object.

    Returns:
        bool: True if the user has permission, False otherwise.
    """
    def has_permission(self, request, view):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        if user.verified:
            return True
        return False
