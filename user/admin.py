from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(StaffProfile)
admin.site.register(Doctor)
admin.site.register(DoctorProfile)
admin.site.register(pharmacyReport)
admin.site.register(PharmacyProfile)
admin.site.register(UserDevice)

@admin.register(Pharmacy)
class PharmacyAdmin(ImportExportModelAdmin):
    resource_class = PharmacyResource 
    list_display = ('name', 'phone_number', 'status', 'created_at')
    search_fields = ('name', 'phone_number')