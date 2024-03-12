from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializers


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializers
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
