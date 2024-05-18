from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Habit(models.Model):
    """Модель - привычка"""

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1,
                               verbose_name="Автор", related_name='habit')
    place = models.CharField(max_length=50, verbose_name='Место выполнения')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=150, verbose_name='Действие')
    pleasant = models.BooleanField(default=False, verbose_name='Признак приятности')
    related_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Связанная привычка')
    periodicity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)], default=1,
                                              verbose_name='Периодичность')
    reward = models.CharField(max_length=100, null=True, blank=True, verbose_name='Вознаграждение')
    complete_time = models.DateTimeField(default=timezone.now, verbose_name='Время выполнения')
    is_public = models.BooleanField(default=False, verbose_name='Признак публикации')
    next_date = models.DateField(null=True, blank=True,  verbose_name="дата следующего действия")

    def __str__(self):
        return f'{self.action}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['id']

    constraints = [
        models.CheckConstraint(
            check=models.Q(
                pleasant=False, related_habit__isnull=True, reward__isnull=False
            ) | models.Q(
                pleasant=False, related_habit__isnull=False, reward__isnull=True
            ) | models.Q(
                pleasant=True, related_habit__isnull=True, reward__isnull=True
            ),
            name='either_related_habit_or_reward_or_pleasant_habit'
        )
    ]
