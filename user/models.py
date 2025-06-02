from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from .managers import StaffManager, DoctorManager, PharmacyManager,IPatientManager
from django.utils import timezone

class CustomUser(AbstractUser):

    class Gender(models.TextChoices):
        MALE = 'Male',
        FEMALE = 'Female',
        OTHER = 'Other',
    class Status(models.TextChoices):
        ACTIVE = 'Active',
        DEACTIVE = 'Deactive',
    
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    last_name = None
    first_name = None
    phone_number = models.CharField(max_length=15, null=True, blank=True,unique=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    avatar=models.ImageField(upload_to='profile_pic',null=True,blank=True)
    gender = models.CharField(max_length=6, choices=Gender.choices, default=Gender.MALE, null=True, blank=True)
    email = models.EmailField(verbose_name='Email Address', null=True,blank=True)
    nid=models.CharField(max_length=50, null=True, blank=True)
    user_id=models.IntegerField(null=True,blank=True,unique=True)
    barcode=models.ImageField(blank=True,null=True,upload_to='barcode')
    status=models.CharField(max_length=8, choices=Status.choices, default=Status.ACTIVE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,related_name='+')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,related_name='+')

    def __str__(self):
        return str(self.phone_number)
    
    
class UserDevice(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_f_token")
    fcm_token = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.phone_number}'s device"
    
    
class Staff(CustomUser):
    class Meta:
        proxy = True

    objects = StaffManager()

    def save(self, *args, **kwargs):
        super(Staff, self).save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name='staff')
        self.groups.set([group])

class Doctor(CustomUser):
    class Meta:
        proxy = True

    objects = DoctorManager()

    def save(self, *args, **kwargs):
        super(Doctor, self).save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name='doctor')
        self.groups.set([group])


class Pharmacy(CustomUser):
    class Meta:
        proxy = True

    objects = PharmacyManager()

    def save(self, *args, **kwargs):
        super(Pharmacy, self).save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name='pharmacy')
        self.groups.set([group])


class IPatient(CustomUser):
    class Meta:
        proxy = True

    objects = IPatientManager()

    def save(self, *args, **kwargs):
        super(IPatient, self).save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name='ipatient')
        self.groups.set([group])
        
class StaffProfile(models.Model):
    
    class Role_Type(models.TextChoices):
        Accountant = 'Accountant', 'Accountant'
        HR = 'HR', 'HR'
        Manager = 'Manager', 'Manager'
        CP = 'CP', 'CP'
        
    staff_field = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='staff_profile')
    designation=models.CharField(max_length=50,null=True,blank=True)
    is_staff = models.BooleanField(default=True)
    role=models.CharField(max_length=30, choices=Role_Type.choices,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.staff_field.name)
    
class DoctorProfile(models.Model):
    AVAILABILITY_STATUS = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('service', 'Service'),
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    doctor_field = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name='doc_profile') 
    specialization = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    cirtification = models.ImageField(upload_to='certificate', null=True, blank=True)
    working_status = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='available')
    last_call_ended = models.DateTimeField(null=True, blank=True)  # Track last call end time
    bmdc_no = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def is_available(self):
        return self.status == 'available'

    def mark_busy(self):
        self.update_status('busy')

    def mark_offline(self):
        self.update_status('offline')

    def mark_online(self):
        self.update_status('online')

    def mark_service(self):
        self.update_status('service')

    def mark_available(self):
        self.update_status('available')

    @classmethod
    def get_available_doctor(cls):
        return cls.objects.filter(status='available').first()
    @classmethod
    def count_available_doctors(cls):
        return cls.objects.filter(status='available').count()

    def __str__(self):
        return str(self.doctor_field.name)

    
class  PharmacyProfile(models.Model):
    pharmacy_field = models.OneToOneField(Pharmacy, on_delete=models.CASCADE, related_name='pharma_profile')
    cirtification =models.ImageField(upload_to='cirtificate',null=True,blank=True)
    post=models.CharField(max_length=50,null=True,blank=True)
    thana_or_upazila=models.CharField(max_length=50,null=True,blank=True)
    district=models.CharField(max_length=50,null=True,blank=True)
    division=models.CharField(max_length=50,null=True,blank=True)
    referral = models.OneToOneField(Staff, on_delete=models.SET_NULL,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return str(self.pharmacy_field.name) 
    

class  IPatientProfile(models.Model):
    patient_field = models.OneToOneField(IPatient, on_delete=models.CASCADE, related_name='ipatient_profile')
    age=models.CharField(max_length=50,null=True,blank=True)
    weight= models.FloatField(null=True,blank=True)
    bmi =models.CharField(max_length=50,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pharmacy_field.name)
    
class PatientReport(models.Model):
    patient_id = models.ForeignKey(IPatient, on_delete=models.CASCADE, related_name='patient_reports')
    report_file = models.FileField(upload_to='patient_reports/', null=True, blank=True)
    report_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_name} - {self.patient.name or self.patient.phone_number}"
    
class pharmacyReport(models.Model):
    pharmacy_id = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='pharmacy_reports')
    report_file = models.FileField(upload_to='patient_reports/', null=True, blank=True)
    patient_mobile =models.CharField(max_length=15, null=True, blank=True)
    report_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_name} - {self.patient_mobile or self.pharmacy_id.name}"

    

