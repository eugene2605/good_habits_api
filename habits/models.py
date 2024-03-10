from django.db import models


class Habit(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='создатель привычки')
    place = models.CharField(max_length=150, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=200, verbose_name='действие')
    is_nice_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='связанная привычка')
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='периодичность в днях')
    reward = models.CharField(max_length=200, null=True, blank=True, verbose_name='вознаграждение')
    time_to_complete = models.PositiveSmallIntegerField(verbose_name='время на выполнение в секундах')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    last_message_sent = models.DateTimeField(null=True, blank=True, verbose_name='последняя отправка сообщения')

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('user',)
