from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Teacher, Room, Lesson
from .serializers import TeacherSerializer, RoomSerializer, LessonSerializer, ScheduleDataSerializer, AICommandSerializer
from .ai_service import ScheduleAIService

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    
    @action(detail=False, methods=['get'])
    def by_day(self, request):
        day = request.query_params.get('day')
        if not day:
            return Response({'error': 'Day required'}, status=400)
        lessons = Lesson.objects.filter(day=day)
        return Response(self.get_serializer(lessons, many=True).data)
    
    @action(detail=False, methods=['get'])
    def by_teacher(self, request):
        tid = request.query_params.get('teacher_id')
        if not tid:
            return Response({'error': 'Teacher ID required'}, status=400)
        lessons = Lesson.objects.filter(teacher_id=tid)
        return Response(self.get_serializer(lessons, many=True).data)
    
    @action(detail=False, methods=['get'])
    def conflicts(self, request):
        conflicts = []
        from django.db.models import Count
        
        dupes = Lesson.objects.values('day', 'slot', 'teacher_id').annotate(
            Count('id')).filter(id__count__gt=1)
        
        for d in dupes:
            conflicts.append({'type': 'teacher', 'day': d['day'], 'slot': d['slot']})
        
        dupes = Lesson.objects.values('day', 'slot', 'room_id').annotate(
            Count('id')).filter(id__count__gt=1)
        
        for d in dupes:
            conflicts.append({'type': 'room', 'day': d['day'], 'slot': d['slot']})
        
        return Response(conflicts)

class ScheduleDataAPIView(APIView):
    def get(self, request):
        data = {
            'teachers': Teacher.objects.all(),
            'rooms': Room.objects.all(),
            'lessons': Lesson.objects.all(),
        }
        return Response(ScheduleDataSerializer(data).data)

class AIAdminChatAPIView(APIView):
    def post(self, request):
        ser = AICommandSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        
        try:
            ai = ScheduleAIService()
            result = ai.process_command(ser.validated_data['command'])
            return Response(result)
        except Exception as e:
            
            return Response({'error': str(e)}, status=500)

class BulkDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data.get('lesson_ids', [])
        if not ids:
            return Response({'error': 'No IDs'}, status=400)
        deleted, _ = Lesson.objects.filter(id__in=ids).delete()
        return Response({'deleted': deleted})