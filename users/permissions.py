from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "Это не ваш профиль"

    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.email
