from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner
from habits.serialisers import HabitSerializers


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializers
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user)


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.filter(is_public=True)


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
