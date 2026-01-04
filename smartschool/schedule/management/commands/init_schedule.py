from django.core.management.base import BaseCommand
from schedule.models import Teacher, Room, Lesson

class Command(BaseCommand):
    def handle(self, *args, **options):
        Teacher.objects.all().delete()
        Room.objects.all().delete()
        Lesson.objects.all().delete()
        
        teachers = [
            {'id': 't1', 'name': 'Иван Петров', 'subject': 'Математика', 'email': 'ivan@school.ru'},
            {'id': 't2', 'name': 'Мария Сидорова', 'subject': 'Физика', 'email': 'maria@school.ru'},
            {'id': 't3', 'name': 'Елена Иванова', 'subject': 'История', 'email': 'elena@school.ru'},
            {'id': 't4', 'name': 'Дмитрий Волков', 'subject': 'Физкультура', 'email': 'dmitry@school.ru'},
        ]
        for t in teachers:
            Teacher.objects.create(**t)
        
        rooms = [
            {'id': 'r1', 'number': '101', 'capacity': 30, 'room_type': 'general'},
            {'id': 'r2', 'number': '202', 'capacity': 25, 'room_type': 'lab'},
            {'id': 'r3', 'number': '303', 'capacity': 35, 'room_type': 'general'},
            {'id': 'r4', 'number': 'Спортзал', 'capacity': 100, 'room_type': 'gym'},
        ]
        for r in rooms:
            Room.objects.create(**r)
        
        lessons = [
            {'id': 'l1', 'teacher_id': 't1', 'room_id': 'r1', 'subject': 'Алгебра', 'day': 'Monday', 'slot': 1, 'grade': '10А', 'color': 'indigo'},
            {'id': 'l2', 'teacher_id': 't2', 'room_id': 'r2', 'subject': 'Физика', 'day': 'Monday', 'slot': 2, 'grade': '10А', 'color': 'blue'},
            {'id': 'l3', 'teacher_id': 't3', 'room_id': 'r3', 'subject': 'История', 'day': 'Monday', 'slot': 3, 'grade': '11Б', 'color': 'amber'},
            {'id': 'l4', 'teacher_id': 't4', 'room_id': 'r4', 'subject': 'Физкультура', 'day': 'Tuesday', 'slot': 1, 'grade': '9В', 'color': 'green'},
        ]
        for l in lessons:
            Lesson.objects.create(**l)
        
        self.stdout.write(self.style.SUCCESS('✅ Готово!'))