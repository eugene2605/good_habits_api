from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "Это не ваша привычка"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
