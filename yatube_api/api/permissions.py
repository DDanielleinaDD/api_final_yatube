from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Ограничение для комментариев и постов на чтение или изменение"""
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
