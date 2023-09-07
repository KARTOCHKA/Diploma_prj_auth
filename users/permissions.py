from rest_framework import permissions
from .models import *


class IsVerifiedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print('Verified user comlete!')
            return True
        return False
