from rest_framework import viewsets, generics, permissions

class IsCommercial(permissions.BasePermission):
    """Allow unsafe methods for admin and commercial users only."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.groups.filter(name = 'Commercial') or request.user.is_staff or request.user.is_superuser)
