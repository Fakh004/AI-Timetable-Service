from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('rooms', RoomViewSet, basename='room')
router.register('lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('schedule-data/', ScheduleDataAPIView.as_view()),
    path('ai-command/', AIAdminChatAPIView.as_view()),
    path('lessons/bulk-delete/', BulkDeleteAPIView.as_view()),
]