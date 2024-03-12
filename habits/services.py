import requests

from config import settings

URL = 'https://api.telegram.org/bot'
TOKEN = settings.TELEGRAM_TOKEN


def send_telegram_message(telegram_id, text):
    requests.post(
                url=f'{URL}{TOKEN}/sendMessage',
                data={
                    'chat_id': telegram_id,
                    'text': text
                }
            )
