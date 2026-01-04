from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Teacher(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return f"{self.name} ({self.subject})"

class Room(models.Model):
    ROOM_TYPES = [
        ('general', 'Обычный класс'),
        ('lab', 'Лаборатория'),
        ('gym', 'Спортзал'),
    ]
    
    id = models.CharField(max_length=10, primary_key=True)
    number = models.CharField(max_length=50)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number']
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    def __str__(self):
        return f"Кабинет {self.number}"

class Lesson(models.Model):
    DAYS = [
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
    ]
    
    COLORS = [
        ('indigo', 'Индиго'),
        ('blue', 'Синий'),
        ('green', 'Зеленый'),
        ('amber', 'Янтарный'),
        ('rose', 'Роза'),
        ('cyan', 'Голубой'),
        ('emerald', 'Изумруд'),
        ('violet', 'Фиолетовый'),
    ]

    id = models.CharField(max_length=10, primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='lessons')
    subject = models.CharField(max_length=255)
    day = models.CharField(max_length=20, choices=DAYS)
    slot = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    grade = models.CharField(max_length=10)
    color = models.CharField(max_length=20, choices=COLORS, default='indigo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day', 'slot']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        # constraints = [
        #     models.UniqueConstraint(fields=['teacher', 'day', 'slot'], name='unique_teacher_schedule'),
        #     models.UniqueConstraint(fields=['room', 'day', 'slot'], name='unique_room_schedule'),
        # ]

    def __str__(self):
        return f"{self.subject} - {self.grade} ({self.day} {self.slot})"