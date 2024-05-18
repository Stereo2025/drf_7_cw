import re

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""
    password = serializers.CharField(min_length=8, write_only=True)
    telegram_id = serializers.IntegerField(write_only=True, required=False)

    def create(self, validated_data):
        """Метод для создания пользователя"""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            telegram_id=validated_data.get('telegram_id')
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'telegram_id')

    def validate_password(self, value):
        """Валидатор пароля"""
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен содержать минимум 8 символов.")

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")

        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну строчную букву.")

        if not re.search(r'\d', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру.")

        if not re.search(r'[@$!%*?&]', value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы один специальный символ (@, $, !, %, *, ?, &).")

        if 'password' in value.lower():
            raise serializers.ValidationError("Пароль не должен содержать слово 'password'.")

        return value