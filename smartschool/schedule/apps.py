# from django.apps import AppConfig


# class ScheduleConfig(AppConfig):
#     name = 'schedule'

from django.apps import AppConfig

class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schedule'
    verbose_name = 'Расписание'