from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_meeting, name='create_meeting'),
    path('meeting/<str:meeting_id>/', views.meeting_room, name='meeting_room'),
    path('test/<str:preset_name>/', views.test, name='test'),
]