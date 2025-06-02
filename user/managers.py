from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.db import models


class StaffManager(BaseUserManager):
    def get_queryset(self):
        return super(StaffManager, self).get_queryset().filter(groups__name='staff')


class DoctorManager(BaseUserManager):
    def get_queryset(self):
        return super(DoctorManager, self).get_queryset().filter(groups__name='doctor')


class PharmacyManager(BaseUserManager):
    def get_queryset(self):
        return super(PharmacyManager, self).get_queryset().filter(groups__name='pharmacy')
    
class IPatientManager(BaseUserManager):
    def get_queryset(self):
        return super(IPatientManager, self).get_queryset().filter(groups__name='ipatient')

