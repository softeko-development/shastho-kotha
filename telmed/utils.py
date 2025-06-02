from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def broadcast_doctor_request_update(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "doctor_requests_group",
        {
            "type": "send_update",
            "data": {
                "id": request.id,
                "patient_number": request.patient.patient_phone_no,
                "status": request.status
            }
        }
    )
