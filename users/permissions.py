from rest_framework import permissions


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
        if request.user.is_authenticated:
            return True
        return False
