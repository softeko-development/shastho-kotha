from django import forms
from .models import Pharmaceutical_Companies, Generics_Names, Dosage_Form, Med_Category, Test_category, Test_name, ConditionInstruction, Brand_name

class PharmaceuticalCompanyForm(forms.ModelForm):
    class Meta:
        model = Pharmaceutical_Companies
        fields = ['name', 'logo']

class GenericsForm(forms.ModelForm):
    class Meta:
        model = Generics_Names
        fields = ['name']

class Dosage_Form_Form(forms.ModelForm):
    class Meta:
        model = Dosage_Form
        fields = ['name']

class MedCategoryForm(forms.ModelForm):
    class Meta:
        model = Med_Category
        fields = ['name']

class TestCategoryForm(forms.ModelForm):
    class Meta:
        model = Test_category
        fields = ['name']


class TestNameForm(forms.ModelForm):
    class Meta:
        model = Test_name
        fields = ['name', 'test_cat_name']

class ConditionInstructionForm(forms.ModelForm):
    class Meta:
        model = ConditionInstruction
        fields = ['instruction']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Brand_name
        fields = ['item_code', 'name', 'strength', 'category', 'pharmaceutical_com_id', 'generics_id', 'dosage_form_id']
        
