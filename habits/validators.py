from rest_framework import serializers
from datetime import timedelta

from habits.models import Habit
from habits.variables import ERROR_BOTH_HABIT_AND_REWARD, ERROR_LONG_EXECUTION_TIME, ERROR_UNPLEASANT_RELATED_HABIT, \
    ERROR_PLEASANT_WITH_BONUS, ERROR_COMPLETION_DURATION


def validate_non_coexisting_habit_and_reward(value):
    """
    Проверяет, что не указывается одновременно связанная привычка и вознаграждение.
    """
    related_habit = value.get("related_habit")
    reward = value.get("reward")
    if related_habit and reward:
        raise serializers.ValidationError(ERROR_BOTH_HABIT_AND_REWARD)


def validate_execution_time(value):
    """
    Проверяет, что время выполнения не превышает 180 секунд.
    """
    time_to_complete = value.get('time_to_complete')
    if time_to_complete and time_to_complete > timedelta(minutes=3):
        raise serializers.ValidationError(ERROR_LONG_EXECUTION_TIME)


def validate_related_habit_pleasantness(value):
    """
    Проверяет, что связанные привычки имеют признак приятной привычки.
    """
    related_habit = value.get("related_habit")
    if related_habit and not related_habit.sign_of_pleasant:
        raise serializers.ValidationError(ERROR_UNPLEASANT_RELATED_HABIT)


def validate_pleasant_habit(value):
    """
    Проверяет, что у приятной привычки отсутствует вознаграждение и связанная привычка.
    """
    sign_of_pleasant = value.get("sign_of_pleasant")
    reward = value.get("reward")
    related_habit = value.get("related_habit")
    if sign_of_pleasant and (reward or related_habit):
        raise serializers.ValidationError(ERROR_PLEASANT_WITH_BONUS)


def validate_completion_periodicity(value):
    """
    Проверяет выполнение привычки не реже раза в 7 дней.
    """
    periodicity = value.get("periodicity")
    if periodicity and periodicity > 7:
        raise serializers.ValidationError(ERROR_COMPLETION_DURATION)


class CustomSerializer(serializers.Serializer):
    related_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), required=False)
    reward = serializers.CharField(required=False)
    time_to_complete = serializers.DurationField()
    sign_of_pleasant = serializers.BooleanField()
    periodicity = serializers.IntegerField()

    def validate(self, data):
        validate_non_coexisting_habit_and_reward(data)
        validate_execution_time(data)
        validate_related_habit_pleasantness(data)
        validate_pleasant_habit(data)
        validate_completion_periodicity(data)
        return data
