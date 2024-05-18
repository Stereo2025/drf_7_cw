import django
django.setup()
from django.test import TestCase
from habits.models import Habit
from users.models import User
from datetime import datetime, timedelta
from unittest import mock
from django.utils import timezone
from habits.telegram_task import create_message, check_and_send_reminders


class TestTelegramMessage(TestCase):

    def setUp(self):

        User.objects.all().delete()
        Habit.objects.all().delete()

        self.user = User.objects.create_user(email='testuser@example.com', password='password123', telegram_id='123456789')

        now = datetime.now()
        now_time = now.time()

        self.unpleasant_habit = Habit.objects.create(
            action="Test Habit",
            place="Test Place",
            time=now_time,
            pleasant=False,
            is_public=True,
            author=self.user,
            periodicity=1,
            next_date=now.date()
        )

    def tearDown(self):
        # Очистка базы данных после каждого теста
        User.objects.all().delete()
        Habit.objects.all().delete()

    @mock.patch('habits.telegram_task.send_telegram_message')
    def test_send_telegram_message_call(self, mock_send_telegram_message):
        chat_id = '123456789'
        message = 'Test message'
        bot_token = 'test_token'
        mock_send_telegram_message.return_value = None
        # Вызов функции из модуля
        from habits.telegram_task import send_telegram_message as real_send_telegram_message
        real_send_telegram_message(chat_id, message, bot_token)
        # Проверка, что функция была вызвана один раз с указанными аргументами
        mock_send_telegram_message.assert_called_once_with(chat_id, message, bot_token)

    def test_create_message(self):
        habit = self.unpleasant_habit
        habit.action = "Read a book"
        habit.place = "Library"
        habit.time = timezone.now().time()
        habit.reward = "Coffee"

        related_habit = Habit.objects.create(
            action="Workout",
            place="Gym",
            time=timezone.now().time(),
            pleasant=False,
            is_public=False,
            author=self.user
        )

        habit.related_habit = related_habit
        habit.save()

        chat_id, message = create_message(habit)
        expected_message = (f"Напоминание: {habit.action} в {habit.place} в {habit.time.strftime('%H:%M')}."
                            f" Награда за выполнение: {habit.reward}."
                            f" Связанная привычка: {related_habit.action}.")

        self.assertEqual(chat_id, self.user.telegram_id)
        self.assertEqual(message, expected_message)

    def test_check_and_send_reminders(self):
        with mock.patch('habits.telegram_task.create_message') as mock_create_message,\
             mock.patch('habits.telegram_task.send_telegram_message') as mock_send_telegram_message:

            chat_id = '123456789'
            message = 'Reminder message'
            mock_create_message.return_value = (chat_id, message)

            check_and_send_reminders()

            mock_create_message.assert_called_once_with(self.unpleasant_habit)
            mock_send_telegram_message.assert_called_once_with(chat_id, message)

            self.unpleasant_habit.refresh_from_db()
            self.assertEqual(
                self.unpleasant_habit.next_date,
                datetime.now().date() + timedelta(days=1)
            )
