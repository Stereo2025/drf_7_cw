import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
import logging

load_dotenv()
# Настройка логгера
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Создает суперпользователя"

    def handle(self, *args, **options):
        email = os.environ.get('EMAIL_ADMIN')
        password = os.environ.get('PASSWORD_ADMIN')

        if not email or not password:
            logger.error("Необходимо задать EMAIL_ADMIN и PASSWORD_ADMIN в переменных окружения")
            return

        User = get_user_model()
        try:
            user = User.objects.create(
                email=email,
                first_name='Anton',
                last_name='Evgeni4',
                is_staff=True,
                is_superuser=True
            )
            user.set_password(password)
            user.save()
            logger.info(f"Создан суперпользователь {email}")
        except Exception as e:
            logger.error(f"Произошла ошибка при создании пользователя: {str(e)}")