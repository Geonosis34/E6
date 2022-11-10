from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('chat/', views.room_view, name='room'),
    path('chat/<str:room_name>/', views.chat_view, name='chat'),
]
