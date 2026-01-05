import json
import google.generativeai as genai
from decouple import config
from .models import Teacher, Room, Lesson
from django.db.models import F
import random

class ScheduleAIService:
    def __init__(self):
        """Инициализация с API ключом Gemini"""
        self.api_key = config('GEMINI_API_KEY', default='')
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def get_current_state(self):
        """Получаем текущее состояние расписания"""
        teachers = list(Teacher.objects.all().values('id', 'name', 'subject', 'email'))
        rooms = list(Room.objects.all().values('id', 'number', 'capacity').annotate(type=F('room_type')))
        lessons = list(Lesson.objects.all().values(
            'id', 'subject', 'day', 'slot', 'grade', 'color'
        ).annotate(
            teacherId=F('teacher_id'),
            roomId=F('room_id')
        ))

        return {
            'teachers': teachers,
            'rooms': rooms,
            'lessons': lessons,
        }

    def process_command(self, command: str):
        """Обрабатываем команду через AI полностью"""
        try:
            current_data = self.get_current_state()
            result = self._process_with_ai(command, current_data)

            # Сохраняем изменения только если AI вернул что-то полезное
            if 'updatedData' in result and result['updatedData'].get('lessons'):
                self._apply_changes(result['updatedData'])
            return result

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'updatedData': self.get_current_state(),
                'explanation': f"❌ Ошибка: {str(e)}"
            }

    def _process_with_ai(self, command: str, current_data: dict = None):
        """Обработка команды через AI Gemini"""
        current_data = self.get_current_state() if current_data is None else current_data

        # Усиленный prompt, чтобы AI всегда возвращал нужные поля
        prompt = f"""
Ты помощник по управлению школьным расписанием.
Текущее состояние:
Учителя: {json.dumps(current_data['teachers'], ensure_ascii=False)}
Кабинеты: {json.dumps(current_data['rooms'], ensure_ascii=False)}
Уроки: {json.dumps(current_data['lessons'], ensure_ascii=False)}

Команда пользователя: "{command}"

Обязательные поля для каждого урока:
id, teacherId, roomId, subject, day, slot (1-8), grade, color

Используй только уникальные строковые ID для новых объектов:
Учителя: t1, t2, ...
Кабинеты: r1, r2, ...
Уроки: l1, l2, ...

Верни ТОЛЬКО JSON без пояснений:
{{
  "updatedData": {{
    "teachers": [...],
    "rooms": [...],
    "lessons": [...]
  }},
  "explanation": "краткое пояснение, или то что просит пользователь в челове"
}}
"""
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt, generation_config={'temperature': 0.3})
            text = response.text.strip()

            # Убираем markdown
            if text.startswith('```json'):
                text = text[7:]
            elif text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()

            result = json.loads(text)

            # Проверяем структуру
            if 'updatedData' not in result or 'explanation' not in result:
                raise ValueError("AI вернул некорректный JSON")

            return result

        except Exception as e:
            import traceback
            traceback.print_exc()
            # Возвращаем текущее состояние при ошибке
            return {
                'updatedData': current_data,
                'explanation': f"❌ AI ошибка: {str(e)}"
            }

    def _apply_changes(self, data: dict):
        """Применяем изменения в БД"""
        try:
            # Учителя
            for teacher in data.get('teachers', []):
                if not all(k in teacher for k in ('id', 'name', 'subject')):
                    print(f"⚠️ Учитель пропущен, нет обязательных полей: {teacher}")
                    continue
                Teacher.objects.update_or_create(
                    id=teacher['id'],
                    defaults={
                        'name': teacher['name'],
                        'subject': teacher['subject'],
                        'email': teacher.get('email', ''),
                    }
                )

            # Кабинеты
            for room in data.get('rooms', []):
                if not all(k in room for k in ('id', 'number', 'capacity')):
                    print(f"⚠️ Кабинет пропущен, нет обязательных полей: {room}")
                    continue
                room_obj, created = Room.objects.get_or_create(
                    id=room['id'],
                    defaults={
                        'number': room['number'],
                        'capacity': room['capacity'],
                        'room_type': room.get('type', 'general')
                    }
                )
                if not created:
                    room_obj.capacity = room['capacity']
                    room_obj.room_type = room.get('type', 'general')
                    room_obj.save(update_fields=['capacity', 'room_type'])

            # Уроки
            REQUIRED_FIELDS = {'id', 'teacherId', 'roomId', 'subject', 'day', 'slot', 'grade'}

            for lesson in data.get('lessons', []):
                missing = REQUIRED_FIELDS - lesson.keys()
                if missing:
                    print(f"⚠️ Урок пропущен, нет обязательных полей {missing}: {lesson}")
                    continue

                Lesson.objects.update_or_create(
                    id=lesson['id'],
                    defaults={
                        'teacher_id': lesson['teacherId'],
                        'room_id': lesson['roomId'],
                        'subject': lesson['subject'],
                        'day': lesson['day'],
                        'slot': lesson['slot'],
                        'grade': lesson['grade'],
                        'color': lesson.get('color', 'indigo')
                    }
                )

            print("✅ БД обновлена успешно")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ Ошибка при обновлении БД: {str(e)}")


