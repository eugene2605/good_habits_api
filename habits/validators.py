from rest_framework.serializers import ValidationError


class RelatedHabitOrRewardValidator:

    def __init__(self, fields):
        self.related_habit, self.reward = fields

    def __call__(self, value):
        value_related_habit = dict(value).get(self.related_habit)
        value_reward = dict(value).get(self.reward)
        if value_related_habit and value_reward:
            raise ValidationError('Нельзя указывать одновременно связанную привычку и вознаграждение')


class TimeToCompleteValidator:

    def __init__(self, fields):
        self.time_to_complete = fields

    def __call__(self, value):
        value_time_to_complete = dict(value).get(self.time_to_complete)
        if value_time_to_complete:  # добавляет необязательность заполнения поля при изменении записи
            if int(value_time_to_complete) > 120:
                raise ValidationError('Время выполнения должно быть не больше 120 секунд')


class RelatedHabitValidator:

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        value_related_habit = dict(value).get(self.fields)
        if value_related_habit:
            if not value_related_habit.__dict__['is_nice_habit']:
                raise ValidationError('В связанные привычки могут попадать только приятные привычки')


class IsNiceHabitValidator:

    def __init__(self, fields):
        self.is_nice_habit, self.related_habit, self.reward = fields

    def __call__(self, value):
        value_is_nice_habit = dict(value).get(self.is_nice_habit)
        value_related_habit = dict(value).get(self.related_habit)
        value_reward = dict(value).get(self.reward)
        if value_is_nice_habit:
            if value_related_habit or value_reward:
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')


class PeriodicityValidator:

    def __init__(self, fields):
        self.periodicity = fields

    def __call__(self, value):
        value_periodicity = dict(value).get(self.periodicity)
        if value_periodicity:  # добавляет необязательность заполнения поля при изменении записи
            if int(value_periodicity) > 7:
                raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')
