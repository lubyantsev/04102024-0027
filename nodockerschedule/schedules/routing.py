from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/schedule/<int:schedule_id>/', consumers.ScheduleConsumer.as_asgi()),
    ]
