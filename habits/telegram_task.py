import requests
from celery import shared_task
from datetime import datetime, timedelta
import logging
from habits.models import Habit
from config import settings

logger = logging.getLogger(__name__)

bot_token = settings.TELEGRAM_API_TOKEN


def send_telegram_message(telegram_id, message, bot_token):
    """
    Отправка сообщения в телеграм
    """
    URL = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        response = requests.post(
            url=URL,
            data={
                'telegram_id': telegram_id,
                'text': message,
            }
        )
        response.raise_for_status()
        logger.info(f"Message sent to telegram_id: {telegram_id}")
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")


def create_message(habit):
    """Функция создания сообщения"""
    message_parts = [f"Напоминание: {habit.action} в {habit.place} в {habit.time.strftime('%H:%M')}."]

    if habit.reward:
        message_parts.append(f"Награда за выполнение: {habit.reward}.")
    if habit.related_habit:
        related_habit_action = habit.related_habit.action
        message_parts.append(f"Связанная привычка: {related_habit_action}.")

    message = " ".join(message_parts)
    return habit.author.telegram_id, message


@shared_task
def check_and_send_reminders():
    """
    Отправляет напоминания о привычках пользователям через Telegram.
    """
    unsafe_habits = Habit.objects.filter(pleasant=False)
    now = datetime.now()
    now_date = now.date()
    now_time = now.time()

    for habit in unsafe_habits:
        if habit.next_date is None:
            habit_next_datetime = datetime.combine(now_date, habit.time)
        else:
            habit_next_datetime = datetime.combine(habit.next_date, habit.time)

        if habit_next_datetime <= now:
            telegram_id, message = create_message(habit)
            send_telegram_message(telegram_id, message)
            habit.next_date = now_date + timedelta(days=habit.periodicity)
            habit.save()
            logger.info(f"Habit {habit.id} next date updated to {habit.next_date}")

