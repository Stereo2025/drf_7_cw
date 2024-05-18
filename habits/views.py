from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from habits.models import Habit
from habits.pagination import HabitPagination
from habits.serializers import HabitSerializer
from habits.permissions import IsAuthor


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    """Просмотр всех публичных привычек, фильтр по типу и пагинация"""
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pleasant', 'is_public']

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by('id')


class AuthorHabitListAPIView(generics.ListAPIView):
    """Просмотр всех привычек пользователя, но не более 5 на странице"""
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        return Habit.objects.filter(author=self.request.user)


class HabitRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование и удаление привычки по ID"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]

