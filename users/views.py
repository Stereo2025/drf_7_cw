from rest_framework import generics
from rest_framework.permissions import AllowAny


from users.serializers import UserSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    """Эндпоинт для создания пользователя"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
