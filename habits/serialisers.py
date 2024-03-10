from rest_framework import serializers

from habits.models import Habit
from habits.validators import RelatedHabitOrRewardValidator, TimeToCompleteValidator, RelatedHabitValidator, \
    IsNiceHabitValidator, PeriodicityValidator


class HabitSerializers(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedHabitOrRewardValidator(fields=['related_habit', 'reward']),
            TimeToCompleteValidator(fields='time_to_complete'),
            RelatedHabitValidator(fields='related_habit'),
            IsNiceHabitValidator(fields=['is_nice_habit', 'related_habit', 'reward']),
            PeriodicityValidator(fields='periodicity   ')
        ]
