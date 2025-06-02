from django import forms
from .models import Staff,StaffProfile,Doctor,DoctorProfile,Pharmacy,PharmacyProfile
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class StaffRegistrationForm(UserCreationForm):
    password1 = None
    password2 = None
    class Meta:
        model = Staff
        fields = [
            'username','phone_number','name','avatar','gender','email','nid','user_id'
        ]

 
class StaffEditRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Staff
        fields = [
            'phone_number','name','avatar','gender','email','nid'
        ]


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = [
            'designation', 'role'
        ]
        
class DoctorRegistrationForm(UserCreationForm):
    password1 = None
    password2 = None
    class Meta:
        model = Doctor
        fields = [
            'username','phone_number','name','avatar','gender','email','nid','user_id'
        ]

 
class DoctorEditRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Doctor
        fields = [
            'phone_number','name','avatar','gender','email','nid'
        ]

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = [
            'specialization', 'education','designation', 'cirtification', 'bmdc_no'
        ]
        
class PharmacyRegistrationForm(UserCreationForm):
    password1 = None
    password2 = None
    class Meta:
        model = Pharmacy
        fields = [
            'username','phone_number','name','avatar','gender','email','nid','user_id'
        ]

 
class PharmacyEditRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Pharmacy
        fields = [
            'phone_number','name','avatar','email'
        ]


class PharmacyProfileForm(forms.ModelForm):
    class Meta:
        model = PharmacyProfile
        fields = [
            'cirtification', 'post', 'thana_or_upazila', 'district', 'division'
        ]