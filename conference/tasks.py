# conference/tasks.py
from celery import shared_task
from .models import CallRecord, DoctorProfile
from django.db.models import Q

@shared_task
def update_doctor_status():
    doctors = DoctorProfile.objects.filter(Q(working_status=True) & Q(status='online'))
    for doctor in doctors:
        has_calls = CallRecord.objects.filter(status__in=['scheduled', 'initiated']).exists()
        
        if not has_calls:
            if doctor.status != 'service':
                doctor.mark_available()
        else:
            doctor.mark_service()
    return "Doctor statuses updated"
