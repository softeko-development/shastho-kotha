from .models import *
from import_export import resources

class DosageFormResource(resources.ModelResource):
    class Meta:
        model = Dosage_Form
        fields = ('name')
        
        
class GenericsNamesResource(resources.ModelResource):
    class Meta:
        model = Generics_Names
        fields = ('name')
        
        
class PharmaceuticalCompaniesResource(resources.ModelResource):
    class Meta:
        model = Pharmaceutical_Companies
        fields = ('name','logo')
        
class TestCategoryResource(resources.ModelResource):
    class Meta:
        model = Test_category
        fields = ('name')
        
class ConditionInstructionResource(resources.ModelResource):
    class Meta:
        model = ConditionInstruction
        fields = ('instruction')