from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Teacher, Room, Lesson
from .serializers import TeacherSerializer, RoomSerializer, LessonSerializer
from .ai_service import ScheduleAIService
import json

def index(request):
    """Главная страница с расписанием"""
    teachers = Teacher.objects.all()
    rooms = Room.objects.all()
    lessons = Lesson.objects.all()
    
    # Получаем все классы
    grades = list(set(lesson.grade for lesson in lessons))
    grades.sort()
    
    context = {
        'teachers': TeacherSerializer(teachers, many=True).data,
        'rooms': RoomSerializer(rooms, many=True).data,
        'lessons': LessonSerializer(lessons, many=True).data,
        'grades': grades,
    }
    
    return render(request, 'schedule/index.html', context)

def admin_panel(request):
    """Админ панель"""
    teachers = Teacher.objects.all()
    rooms = Room.objects.all()
    lessons = Lesson.objects.all()
    
    context = {
        'teachers': TeacherSerializer(teachers, many=True).data,
        'rooms': RoomSerializer(rooms, many=True).data,
        'lessons': LessonSerializer(lessons, many=True).data,
    }
    
    return render(request, 'schedule/admin.html', context)

@require_http_methods(["POST"])
def ai_command(request):
    """API для AI команд"""
    try:
        import json
        data = json.loads(request.body)
        command = data.get('command', '')
        
        if not command:
            return JsonResponse({'error': 'Команда не указана'}, status=400)
        
        ai_service = ScheduleAIService()
        result = ai_service._process_with_ai(command)
        
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный JSON'}, status=400)
    except Exception as e:
        import traceback
        print(f"❌ Ошибка в ai_command: {str(e)}")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)