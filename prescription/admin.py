from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *



admin.site.register(Brand_name)
admin.site.register(Test_name)
admin.site.register(Prescription)
admin.site.register(PrescriptionTestSuggest)
admin.site.register(PrescriptionItem)
admin.site.register(PPatient)


@admin.register(Dosage_Form)
class DosageFormAdmin(ImportExportModelAdmin):
    resource_class = DosageFormResource
    list_display = ('name', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name',)
    
    
@admin.register(Generics_Names)
class GenericsNamesAdmin(ImportExportModelAdmin):
    resource_class = GenericsNamesResource
    list_display = ('name', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name',)
    
    
@admin.register(Pharmaceutical_Companies)
class PharmaceuticalCompaniesAdmin(ImportExportModelAdmin):
    resource_class = PharmaceuticalCompaniesResource
    list_display = ('name', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name',)
    
    
@admin.register(Test_category)
class TestCategoryAdmin(ImportExportModelAdmin):
    resource_class = TestCategoryResource
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    
    
@admin.register(ConditionInstruction)
class ConditionInstructionAdmin(ImportExportModelAdmin):
    resource_class = ConditionInstructionResource
    list_display = ('instruction',)
    search_fields = ('instruction',)