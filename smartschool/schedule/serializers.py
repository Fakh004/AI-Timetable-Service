from rest_framework import serializers
from .models import Teacher, Room, Lesson

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subject', 'email']

class RoomSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='room_type')
    
    class Meta:
        model = Room
        fields = ['id', 'number', 'capacity', 'type']

class LessonSerializer(serializers.ModelSerializer):
    teacherId = serializers.CharField(source='teacher_id')
    roomId = serializers.CharField(source='room_id')
    
    class Meta:
        model = Lesson
        fields = ['id', 'teacherId', 'roomId', 'subject', 'day', 'slot', 'grade', 'color']

class ScheduleDataSerializer(serializers.Serializer):
    teachers = TeacherSerializer(many=True)
    rooms = RoomSerializer(many=True)
    lessons = LessonSerializer(many=True)

class AICommandSerializer(serializers.Serializer):
    command = serializers.CharField()