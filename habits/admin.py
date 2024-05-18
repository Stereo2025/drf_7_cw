from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class UsersAdmin(admin.ModelAdmin):
    """Админка модели Habit"""
    list_display = ('author', 'time', 'action', 'pleasant', 'reward', 'complete_time',
                    'place', 'periodicity', 'is_public',)
