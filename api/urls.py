from django.urls import path
from . import views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('messages/', views.MessageView.as_view(), name='api_messages'),
    path('room/', views.RoomView.as_view(), name='api_room'),
    path('schema/',  get_schema_view(title='API Schema',
         description='API for chats'), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='api/docs.html',
        extra_context={'schema_url': 'api_schema'}
    ), name='swagger-ui'),
]
