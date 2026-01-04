from django.contrib import admin
from .models import Teacher, Room, Lesson

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'email')
    search_fields = ('name', 'subject')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'capacity', 'room_type')
    search_fields = ('number',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'grade', 'teacher', 'room', 'day', 'slot')
    search_fields = ('subject', 'grade')
    list_filter = ('day', 'grade')
