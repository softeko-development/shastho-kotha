from django.urls import re_path
from .consumers import DoctorRequestConsumer,DoctorCallNotificationConsumer,QueueUpdateConsumer

websocket_urlpatterns = [
    re_path(r'ws/doctor-requests/(?P<doctor_id>\d+)/$', DoctorRequestConsumer.as_asgi()),
    re_path(r'ws/doctor-calls/(?P<doctor_id>\d+)/$', DoctorCallNotificationConsumer.as_asgi()),
    re_path(r'ws/queue_updates/(?P<user_type>[\w-]+)/$',QueueUpdateConsumer.as_asgi()),
]
