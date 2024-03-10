from datetime import timedelta, datetime, date, timezone
import requests
from celery import shared_task

from config import settings
from habits.models import Habit


URL = 'https://api.telegram.org/bot'
TOKEN = settings.TELEGRAM_TOKEN


@shared_task
def send_message_to_telegram_bot():
    habits = Habit.objects.exclude(is_nice_habit=True)
    for habit in habits:
        if habit.user.telegram_id:
            if not habit.last_message_sent:
                habit.last_message_sent = datetime.combine(date.today(), habit.time)
                now = datetime.now()
            else:
                now = datetime.now(timezone.utc)
            delta_periodicity = timedelta(days=habit.periodicity)
            delta_now = timedelta(minutes=1)
            now_message_sent = habit.last_message_sent + delta_periodicity
            if now - delta_now <= now_message_sent <= now:
                requests.post(
                    url=f'{URL}{TOKEN}/sendMessage',
                    data={
                        'chat_id': habit.user.telegram_id,
                        'text': f'Пришло время для привычки {habit.action}! '
                        f'После выполнения тебя ждет {habit.related_habit if habit.related_habit else habit.reward})'
                    }
                )
                habit.last_message_sent = datetime.combine(date.today(), habit.time)
                habit.save()
