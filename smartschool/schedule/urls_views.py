from django.urls import path
from . import views_template

urlpatterns = [
    path('', views_template.index, name='index'),
    path('admin-panel/', views_template.admin_panel, name='admin_panel'),
    path('api/ai-command/', views_template.ai_command, name='ai_command_page'),
]