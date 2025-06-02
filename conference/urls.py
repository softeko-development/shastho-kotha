from django.urls import path
from .views import *

urlpatterns = [
    path('call_pd/', CallView.as_view(), name='call_pd'),
    path('update-call-status/', UpdateCallStatusView.as_view(), name='update-call-status'),
    path('update-web-call/', UpdateCallWebStatusView.as_view(), name='update-web-call'),
    path('add_doctor_call/', add_doctor_call, name='add_doctor_call'),
    path('call_back/', call_back, name='call_back'),
    # path('api/queue_position/<str:user_type>/<int:user_id>/', QueuePositionView.as_view(), name='queue_position'),
]