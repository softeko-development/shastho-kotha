from django.db import models
from user.models import Doctor, Pharmacy,IPatient
from conference.models import Doctor_Call_serve
from django.db.models.signals import post_save
from django.dispatch import receiver
from telmed.sms import send_sms
from datetime import datetime

class Pharmaceutical_Companies(models.Model):
    name=models.CharField(max_length=70)
    logo=models.ImageField(upload_to='plogo',null=True,blank=True)
    created_by=models.CharField(max_length=20,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__ (self):  
        return self.name
    
class Generics_Names(models.Model):
    name=models.CharField(max_length=100)
    created_by=models.CharField(max_length=20,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.name
    
class Dosage_Form(models.Model):
    name=models.CharField(max_length=80)
    created_by=models.CharField(max_length=20,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.name
    
class Med_Category(models.Model):
    name=models.CharField(max_length=80)
    created_by=models.CharField(max_length=20,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.name
    
class Brand_name(models.Model):
    item_code=models.CharField(max_length=40)
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Med_Category, on_delete=models.CASCADE, related_name='category_med',null=True,blank=True)
    pharmaceutical_com_id= models.ForeignKey(Pharmaceutical_Companies, on_delete=models.CASCADE, related_name='pharmaceutical_med',null=True,blank=True)
    generics_id= models.ForeignKey(Generics_Names, on_delete=models.CASCADE, related_name='generic_med',null=True,blank=True)
    dosage_form_id =models.ForeignKey(Dosage_Form, on_delete=models.CASCADE, related_name='dosage_med',null=True,blank=True)
    strength =models.CharField(max_length=80,null=True,blank=True)
    def __str__ (self):
        return self.name
    
class Test_category(models.Model):
    name=models.CharField(max_length=80)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__ (self):
        return self.name
    
class Test_name(models.Model):
    name=models.CharField(max_length=80)
    test_cat_name=models.ForeignKey(Test_category, on_delete=models.CASCADE, related_name='test_med')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__ (self):
        return self.name
    
class ConditionInstruction(models.Model):
    doctor_id = models.ForeignKey(Doctor,null=True,blank=True, on_delete=models.CASCADE,related_name='doc_contional')
    instruction = models.CharField(max_length=100) 
    label= models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.instruction
    
class PPatient(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male',
        FEMALE = 'Female',
        OTHER = 'Other',
    patient_name = models.CharField(max_length=50,null=True,blank=True)
    patient_phone_no = models.CharField(max_length=15,null=True,blank=True)
    patient_age = models.IntegerField(null=True,blank=True)
    gender = models.CharField(max_length=6, choices=Gender.choices, default=Gender.MALE, null=True, blank=True)
    def __str__(self):
        return self.patient_phone_no
    
    
class Risk_Factor(models.Model):
    name = models.CharField(max_length=60,null=True,blank=True)
    def __str__(self): 
        return self.name

class Prescription(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male',
        FEMALE = 'Female',
        OTHER = 'Other',
    patient_name = models.CharField(max_length=50,null=True,blank=True)
    patient_phone_no = models.CharField(max_length=15,null=True,blank=True)
    patient_age = models.IntegerField(null=True,blank=True)
    gender = models.CharField(max_length=6, choices=Gender.choices, default=Gender.MALE, null=True, blank=True)
    prescription_req = models.ForeignKey(Doctor_Call_serve, on_delete=models.CASCADE, related_name='prescriptions_request')
    prescription_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    drug_history = models.TextField(blank=True, null=True)
    risk_factors = models.TextField(blank=True, null=True)
    problem = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)
    follow_up =models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient_name}"
    
    @property
    def tests(self):
        return self.prescription_tests.all()


class PrescriptionTestSuggest(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='prescription_tests')
    test_name = models.ForeignKey(Test_name, on_delete=models.CASCADE, related_name='test_prescriptions')
    def __str__(self):
        return f"{self.test_name} for Prescription {self.prescription.id}"
    
class PrescriptionItem(models.Model):
    MEAL_INSTRUCTIONS_CHOICES = [
        ('Before Meal', 'Before Meal'),
        ('After Meal', 'After Meal'),
        ('No Meal Instruction', 'No Meal Instruction'),
    ]
    
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE, related_name='items')
    brand_name = models.ForeignKey('Brand_name', on_delete=models.CASCADE)
    dosage = models.CharField(max_length=15, null=True, blank=True)
    dosage_instruction= models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=50)
    meal_instructions = models.CharField(max_length=50, choices=MEAL_INSTRUCTIONS_CHOICES, blank=True, null=True)
    condition_instruction = models.ForeignKey('ConditionInstruction', on_delete=models.SET_NULL, blank=True, null=True)
    additional_instructions = models.TextField(blank=True, null=True)  # Free text for any extra instructions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand_name} for {self.prescription.patient_phone_no}"
    
@receiver(post_save, sender=Doctor_Call_serve)
def check_status_and_send_sms(sender, instance, created, **kwargs):
    if created:
        return
    if instance.status == True:
        prescription = Prescription.objects.filter(prescription_req=instance).first()
        if prescription:
            send_prescription_sms(None, prescription, created=True)

import re

def format_phone_number(phone_number):
    formatted_phone = re.sub(r'^(?:\+?880|0)', '', phone_number)
    return f"880{formatted_phone}"


def send_prescription_sms(sender, instance, created, **kwargs):
    if created:
        doctor_name = instance.prescription_req.doctor.name
        bmdc_number = instance.prescription_req.doctor.doc_profile.bmdc_no
        patient_phone = instance.patient_phone_no
        formatted_phone_number = format_phone_number(patient_phone)
        sms_content = f"Your prescription. {doctor_name}, BMDC: {bmdc_number}, "

        # Adding medicine details
        medicines = instance.items.all()
        if medicines:
            medicine_details = []
            for idx, item in enumerate(medicines, start=1):
                # Handle None strength and meal instructions properly
                strength_display = f"{item.brand_name.strength}" if item.brand_name.strength else ""
                meal_instruction_display = f"{item.get_meal_instructions_display()}" if item.meal_instructions else ""
                
                medicine_details.append(
                    f"{idx}. {item.brand_name.dosage_form_id.name} {item.brand_name.name} {strength_display} {item.dosage or ''} {item.dosage_instruction or ''} {meal_instruction_display} {item.duration} {item.condition_instruction.instruction if item.condition_instruction else ''}".strip()
                )
            sms_content += "Medicine: " + ", ".join(medicine_details) + ", "

        # Adding investigation tests
        investigations = ', '.join([test.test_name.name for test in instance.prescription_tests.all()])
        if investigations:
            sms_content += f"Investigations: {investigations}, "

        # Adding follow-up date
        if instance.follow_up:
            if instance.follow_up != "null 0":
                sms_content += f"Follow-up: {instance.follow_up}, "

        # Append "Powered by Shastokotha"
        sms_content += "Powered by Shastokotha"
        # Removing trailing comma and space
        sms_content = sms_content.strip(", ")

        encoded_sms_content = encode_special_characters(sms_content)
        print(formatted_phone_number)
        send_sms(formatted_phone_number, encoded_sms_content)

def encode_special_characters(message):
    special_characters = {'&': '%26', '$': '%24', '@': '%40', '+': '%2B'}
    for char, encoded_char in special_characters.items():
        message = message.replace(char, encoded_char)
    return message