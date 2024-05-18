from django.contrib import admin

from users.models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    """Админка модели User"""
    list_display = ('pk', 'email', 'phone', 'avatar')
