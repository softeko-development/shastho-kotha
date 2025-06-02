from django.db import models
from user.models import *

class AgoraChannel(models.Model):
    channel_name = models.CharField(max_length=255)
    token_no = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agora Channel: {self.channel_name}"


class CallRecord(models.Model):
    CALL_TYPE_CHOICES = [
        ('direct', 'Direct'),
        ('scheduled', 'Scheduled'),
    ]
    patient_id = models.ForeignKey(IPatient, related_name='patient_call_records',null=True, blank=True, on_delete=models.CASCADE)  
    pharmacy_id = models.ForeignKey(Pharmacy, related_name='pharmacy_call_records',null=True, blank=True, on_delete=models.CASCADE)  
    ppno=models.CharField(max_length=15,null=True,blank=True)
    agora_channel = models.ForeignKey(AgoraChannel, on_delete=models.CASCADE)
    call_type = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES, default='direct')
    call_duration = models.CharField(max_length=10,null=True, blank=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('initiated', 'Initiated'), 
        ('in_progress', 'In Progress'), 
        ('ended', 'Ended'), 
        ('missed', 'Missed'), 
        ('scheduled', 'Scheduled'),

    ], default='initiated')

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Call Record: {self.agora_channel.channel_name} ({self.status})"
    
    def update_call_duration(self, duration):
        if duration:
            self.call_duration = duration
            self.save()
            return True
        return False
    
    def has_scheduled_or_initiated_calls():
        return CallRecord.objects.filter(status__in=['scheduled', 'initiated']).exists()
    
    @classmethod
    def get_queue_position(cls, user_id, user_type):
        
        if user_type == 'patient':
            current_call = cls.objects.filter(patient_id=user_id, status__in=['scheduled', 'initiated']).first()
        elif user_type == 'pharmacy':
            current_call = cls.objects.filter(pharmacy_id=user_id, status__in=['scheduled', 'initiated']).first()
        else:
            raise ValueError("Invalid user type. Must be 'patient' or 'pharmacy'.")

        if current_call:
            queue_position = cls.objects.filter(
                status__in=['scheduled', 'initiated'],
                created_at__lt=current_call.created_at
            ).count()
            return queue_position
        else:
            return 0
        



class Doctor_Call_serve(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='doctor_call_records', null=True, on_delete=models.SET_NULL)
    call_record = models.ForeignKey(CallRecord, related_name='doc_call_id', null=True, on_delete=models.SET_NULL)
    status =models.BooleanField(default=False)
    rejected=models.CharField(max_length=100, null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.call_record:
            return f"Doctor_Call Record: {self.doctor.name} - {self.call_record.ppno} - {str(self.id)}"
        else:
            return f"Doctor_Call Record: {self.doctor.name} (No Call Record)"
    
    def change_status(self, new_status=None):
        
        if new_status is not None:
            self.status = new_status
        else:
            self.status = not self.status
        self.save()
        return self.status
    
    def update_rejected_reason(self, reason):
        
        if reason:
            self.rejected = reason
            self.save()
            return True
        return False
    