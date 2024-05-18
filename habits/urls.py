from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, PublicHabitListAPIView, AuthorHabitListAPIView, \
    HabitRetrieveUpdateDestroyView

app_name = HabitsConfig.name


urlpatterns = [
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits/public/', PublicHabitListAPIView.as_view(), name='public-habit-list'),
    path('habits/user/', AuthorHabitListAPIView.as_view(), name='owner-habit-list'),
    path('habits/<int:pk>/', HabitRetrieveUpdateDestroyView.as_view(), name='habit-detail'),
]

"""
1. Создание привычки:** 
   - URL: `/habits/create/`
   - View: `HabitCreateAPIView`
   - Имя: `'habit-create'`

2. Просмотр публичных привычек с параметрами фильтрации:**
   - URL: `/habits/public/`
   - View: `PublicHabitListAPIView`
   - Имя: `'public-habit-list'`

3. Просмотр привычек текущего пользователя:**
   - URL: `/habits/user/`
   - View: `OwnerHabitListAPIView`
   - Имя: `'owner-habit-list'`

4. Просмотр, редактирование и удаление привычки по ID:**
   - URL: `/habits/<int:pk>/`
   - View: `HabitRetrieveUpdateDestroyView`
   - Имя: `'habit-detail'`
"""
