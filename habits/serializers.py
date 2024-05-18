from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_non_coexisting_habit_and_reward, validate_execution_time, \
    validate_related_habit_pleasantness, validate_pleasant_habit, validate_completion_periodicity


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для привычки
    """

    class Meta:
        model = Habit
        fields = '__all__'
        """
        Валидация для сериализатора
        """
        validators = [
            validate_non_coexisting_habit_and_reward, validate_execution_time,
            validate_related_habit_pleasantness, validate_pleasant_habit, validate_completion_periodicity,
        ]
