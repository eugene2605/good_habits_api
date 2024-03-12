from datetime import timedelta, datetime, date
from django.utils import timezone
from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_message_to_telegram_bot():
    habits = Habit.objects.select_related('user').filter(
        is_nice_habit=False,
        user__telegram_id__isnull=False,
    )
    for habit in habits:
        if not habit.last_message_sent:
            habit.last_message_sent = datetime.combine(date.today(), habit.time)
        now = timezone.now()
        delta_periodicity = timedelta(days=habit.periodicity)
        delta_now = timedelta(minutes=1)
        now_message_sent = habit.last_message_sent + delta_periodicity
        if now - delta_now <= now_message_sent <= now:
            send_telegram_message(
                habit.user.telegram_id,
                f'Пришло время для привычки {habit.action}! '
                f'После выполнения тебя ждет {habit.related_habit if habit.related_habit else habit.reward})'
            )
            habit.last_message_sent = datetime.combine(date.today(), habit.time)
            habit.save()
