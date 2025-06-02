from django.shortcuts import get_object_or_404
from .models import DoctorProfile

def doctor_profile_processor(request):
    doctor_profile = None
    if request.user.is_authenticated:
        try:
            doctor_profile = DoctorProfile.objects.get(doctor_field=request.user)
        except DoctorProfile.DoesNotExist:
            doctor_profile = None
    
    return {'doctor_profile': doctor_profile}