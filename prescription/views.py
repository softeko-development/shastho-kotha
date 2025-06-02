from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets,filters
from rest_framework.permissions import IsAuthenticated
from .models import Brand_name
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render, get_object_or_404,redirect
from user.models import Doctor, Pharmacy
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import  mixins, status
from rest_framework.generics import GenericAPIView
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from .forms import *
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
import uuid
from django.contrib import messages
from tablib import Dataset
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.contrib.auth.decorators import user_passes_test, login_required
from user.decorators import *
from django.utils.decorators import method_decorator
from .pdf_generator import generate_prescription_pdf
from django.utils import timezone
from datetime import timedelta
from conference.models import CallRecord,AgoraChannel,Doctor_Call_serve

@login_required(login_url='login_page_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def product(request):
    productCategories = Med_Category.objects.all().values()
    companies = Pharmaceutical_Companies.objects.all().values()
    generics = Generics_Names.objects.all().values()
    dosages = Dosage_Form.objects.all().values()
    context = {
        'heading': "Product",
        'productCategories': productCategories,
        'companies': companies,
        'generics': generics,
        'dosages': dosages
    }
    return render(request, 'medicine/product/product.html', context)

def generate_item_code():
    # Generates a unique item code using UUID
    return str(uuid.uuid4())[:8].upper()

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def brand_name_import_data(request):
    if request.method == 'POST':
        new_file = request.FILES['file']
        dataset = Dataset()

        if not new_file.name.endswith('.xlsx'):
            messages.error(request, 'Please upload a .xlsx file.')
            return redirect('brand_name_import')

        imported_data = dataset.load(new_file.read(), format='xlsx')

        for data in imported_data:
            name = data[1]
            category_name = data[2]
            pharmaceutical_com_name = data[6]
            generics_name = data[5]
            dosage_form_name = data[3]
            strength = data[4]
            item_code = generate_item_code()
            category = Med_Category.objects.get_or_create(name=category_name)[0] if category_name else None
            pharmaceutical_company = Pharmaceutical_Companies.objects.get_or_create(name=pharmaceutical_com_name)[0] if pharmaceutical_com_name else None
            generics = Generics_Names.objects.get_or_create(name=generics_name)[0] if generics_name else None
            dosage_form = Dosage_Form.objects.get_or_create(name=dosage_form_name)[0] if dosage_form_name else None
            brand_name_instance, created = Brand_name.objects.update_or_create(
                item_code=item_code,
                defaults={
                    'name': name,
                    'category': category,
                    'pharmaceutical_com_id': pharmaceutical_company,
                    'generics_id': generics,
                    'dosage_form_id': dosage_form,
                    'strength': strength if strength else None,
                }
            )

        messages.success(request, 'Brand names have been imported successfully!')
        return redirect('list_brand_names')

    context = {
        'heading': 'Import Brand Names',
    }

    return render(request, 'core/brand_name_import.html', context)


@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def category(request):
    context = {
        'heading': "Category"
    }
    return render(request, 'medicine/category/category.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def menufacturer(request):
    context = {
        'heading': "Menufacturer"
    }
    return render(request, 'medicine/menufacturer/menufacturer.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def generics(request):
    context = {
        'heading': "Generics"
    }
    return render(request, 'medicine/generics/generics.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def test_category(request):
    context = {
        'heading': "Test Category"
    }
    return render(request, 'medicine/test_category/test_category.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def test_name(request):
    testCategories = Test_category.objects.all().values('id', 'name')
    context = {
        'heading': "Test Name",
        'testCategories': testCategories
    }
    return render(request, 'medicine/test_name/test_name.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def dosage_form(request):
    context = {
        'heading': "Dosage Form"
    }
    return render(request, 'medicine/dosage_form/dosage_form.html', context)


def get_user_phone_number(patient_id, pharmacy_id):
    if patient_id:
        patient = IPatient.objects.get(id=patient_id)
        return patient.phone_number if patient else None
    if pharmacy_id:
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        return pharmacy.phone_number if pharmacy else None
    return None

def get_token(agora_channel):
    return "some_generated_token"

def get_group_name(patient_id, pharmacy_id):
    if patient_id:
        return "patient"
    if pharmacy_id:
        return "pharmacy"
    return None

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager']))
def patients_list(request):
    call_records = CallRecord.objects.filter(status__in=['initiated', 'scheduled']).values_list(
        'id', 'patient_id', 'pharmacy_id', 'ppno', 'status', 'agora_channel_id', 'created_at'
    )
    call_notifications = []
    for record in call_records:
        call_id = record[0]
        patient_id = record[1]
        pharmacy_id = record[2]
        ppno = record[3]
        status = record[4]
        agora_channel_id = record[5]
        created_at = record[6]

        try:
            agora_channel = AgoraChannel.objects.get(id=agora_channel_id)
            channel_name = agora_channel.channel_name
            token = agora_channel.token_no
        except AgoraChannel.DoesNotExist:
            channel_name = "Unknown Channel"
            token = "Unknown Token"

        user_phone_number = get_user_phone_number(patient_id, pharmacy_id)
        group_name = get_group_name(patient_id, pharmacy_id)

        notification_data = {
            'id': call_id,
            'user': user_phone_number,
            'call_type': 'scheduled' if status == 'scheduled' else 'direct',
            'status': status,
            'ppno': ppno,
            'channel_name': channel_name,
            'token': token,
            'group': group_name,
            'created_at': created_at
        }

        call_notifications.append(notification_data) 

    context = {
        'call_records': call_notifications,
        'heading': "Patients List"
    }

    return render(request, 'prescription/create_prescription/create_prescription.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager']))
def add_instruction(request):
    context = {
        'heading': "Add Instruction"
    }
    return render(request, 'prescription/add_instruction/add_instruction.html', context)



@method_decorator(login_required(login_url='login_page'), name='dispatch')
@method_decorator(user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager'])), name='dispatch')
class PharmaceuticalCompaniesCRUDView(View):
    
    def get(self, request, *args, **kwargs):
        company_id = kwargs.get('id')
        if company_id:            
            company = get_object_or_404(Pharmaceutical_Companies, id=company_id)
            company_data = {
            'id': company.id,
            'name': company.name,
            'logo': company.logo.url if company.logo else None,
            }
            return JsonResponse(company_data, safe=False)
        # Fetch all companies
        companies = Pharmaceutical_Companies.objects.all().values('id', 'name', 'logo')
        return JsonResponse(list(companies), safe=False)

    def post(self, request, *args, **kwargs):
        company_id = kwargs.get('id')
        if company_id:            
            company = get_object_or_404(Pharmaceutical_Companies, id=company_id)
            form = PharmaceuticalCompanyForm(request.POST, request.FILES, instance=company)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Company updated successfully'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        # Create a new company
        form = PharmaceuticalCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user.username
            company.save()
            return JsonResponse({'status': 'success', 'message': 'Company created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        # Delete a company
        company_id = kwargs.get('id')
        company = get_object_or_404(Pharmaceutical_Companies, id=company_id)
        company.delete()
        return JsonResponse({'status': 'success', 'message': 'Company deleted successfully'})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
@method_decorator(user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager'])), name='dispatch')
class GenericsCRUDView(View):    
    def get(self, request, *args, **kwargs):
        generics_id = kwargs.get('id')
        if generics_id:            
            generics = get_object_or_404(Generics_Names, id=generics_id)
            generics_data = {
            'id': generics.id,
            'name': generics.name,
            }
            return JsonResponse(generics_data, safe=False)
        # Fetch all generics
        generics = Generics_Names.objects.all().values('id', 'name')
        return JsonResponse(list(generics), safe=False)

    def post(self, request, *args, **kwargs):
        generics_id = kwargs.get('id')
        if generics_id:            
            generics = get_object_or_404(Generics_Names, id=generics_id)
            form = GenericsForm(request.POST, instance=generics)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'generics updated successfully'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        # Create a new generics
        form = GenericsForm(request.POST)
        if form.is_valid():
            generics = form.save(commit=False)
            generics.created_by = request.user.username
            generics.save()
            return JsonResponse({'status': 'success', 'message': 'generics created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        # Delete a generics
        generics_id = kwargs.get('id')
        generics = get_object_or_404(Generics_Names, id=generics_id)
        generics.delete()
        return JsonResponse({'status': 'success', 'message': 'generics deleted successfully'})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
@method_decorator(user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager'])), name='dispatch')
class Dosage_FormCRUDView(View):    
    def get(self, request, *args, **kwargs):
        dosage_id = kwargs.get('id')
        if dosage_id:            
            dosage = get_object_or_404(Dosage_Form, id=dosage_id)
            dosage_data = {
            'id': dosage.id,
            'name': dosage.name,
            }
            return JsonResponse(dosage_data, safe=False)
        # Fetch all dosage
        dosage = Dosage_Form.objects.all().values('id', 'name')
        return JsonResponse(list(dosage), safe=False)

    def post(self, request, *args, **kwargs):
        dosage_id = kwargs.get('id')
        if dosage_id:            
            dosage = get_object_or_404(Dosage_Form, id=dosage_id)
            form = Dosage_Form_Form(request.POST, instance=dosage)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Dosage updated successfully'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        # Create a new dosage
        form = Dosage_Form_Form(request.POST)
        if form.is_valid():
            dosage = form.save(commit=False)
            dosage.created_by = request.user.username
            dosage.save()
            return JsonResponse({'status': 'success', 'message': 'Dosage created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        # Delete a dosage
        dosage_id = kwargs.get('id')
        dosage = get_object_or_404(Dosage_Form, id=dosage_id)
        dosage.delete()
        return JsonResponse({'status': 'success', 'message': 'Dosage deleted successfully'})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
@method_decorator(user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager'])), name='dispatch')
class MedCategoryCRUDView(View):    
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('id')
        if category_id:            
            category = get_object_or_404(Med_Category, id=category_id)
            category_data = {
            'id': category.id,
            'name': category.name,
            }
            return JsonResponse(category_data, safe=False)
        # Fetch all category
        category = Med_Category.objects.all().values('id', 'name')
        return JsonResponse(list(category), safe=False)

    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('id')
        if category_id:            
            category = get_object_or_404(Med_Category, id=category_id)
            form = MedCategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'category updated successfully'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        # Create a new category
        form = MedCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user.username
            category.save()
            return JsonResponse({'status': 'success', 'message': 'category created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        # Delete a category
        category_id = kwargs.get('id')
        category = get_object_or_404(Med_Category, id=category_id)
        category.delete()
        return JsonResponse({'status': 'success', 'message': 'category deleted successfully'})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
@method_decorator(user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager'])), name='dispatch')
class TestCategoryCRUDView(View):    
    def get(self, request, *args, **kwargs):
        testCategory_id = kwargs.get('id')
        if testCategory_id:            
            testCategory = get_object_or_404(Test_category, id=testCategory_id)
            testCategory_data = {
            'id': testCategory.id,
            'name': testCategory.name,
            }
            return JsonResponse(testCategory_data, safe=False)
        # Fetch all testCategory
        testCategory = Test_category.objects.all().values('id', 'name')
        return JsonResponse(list(testCategory), safe=False)

    def post(self, request, *args, **kwargs):
        testCategory_id = kwargs.get('id')
        if testCategory_id:            
            testCategory = get_object_or_404(Test_category, id=testCategory_id)
            form = TestCategoryForm(request.POST, instance=testCategory)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'testCategory updated successfully'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        # Create a new testCategory
        form = TestCategoryForm(request.POST)
        if form.is_valid():
            testCategory = form.save(commit=False)
            testCategory.created_by = request.user.username
            testCategory.save()
            return JsonResponse({'status': 'success', 'message': 'testCategory created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        # Delete a testCategory
        testCategory_id = kwargs.get('id')
        testCategory = get_object_or_404(Test_category, id=testCategory_id)
        testCategory.delete()
        return JsonResponse({'status': 'success', 'message': 'testCategory deleted successfully'})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
@method_decorator(user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager'])), name='dispatch')
class TestNameCRUDView(View):    
    def get(self, request, *args, **kwargs):
        testName_id = kwargs.get('id')
        if testName_id:            
            testName = get_object_or_404(Test_name, id=testName_id)
            testName_data = {
            'id': testName.id,
            'name': testName.name,
            'test_cat_id': testName.test_cat_name.id,
            'test_cat_name': testName.test_cat_name.name
            }
            return JsonResponse(testName_data, safe=False)
        # Fetch all testName
        testNames = Test_name.objects.select_related('test_cat_name').values('id', 'name', 'test_cat_name', 'test_cat_name__name')[:50]
        return JsonResponse(list(testNames), safe=False)

    def post(self, request, *args, **kwargs):
        testName_id = kwargs.get('id')
        if testName_id:            
            testName = get_object_or_404(Test_name, id=testName_id)
            form = TestNameForm(request.POST, instance=testName)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'testName updated successfully'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        # Create a new testName
        form = TestNameForm(request.POST)
        if form.is_valid():
            testName = form.save(commit=False)
            testName.created_by = request.user.username
            testName.save()
            return JsonResponse({'status': 'success', 'message': 'testName created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        # Delete a testName
        testName_id = kwargs.get('id')
        testName = get_object_or_404(Test_name, id=testName_id)
        testName.delete()
        return JsonResponse({'status': 'success', 'message': 'testName deleted successfully'})

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def test_name_import_data(request):
    if request.method == 'POST':
        new_file = request.FILES['file']
        dataset = Dataset()

        if not new_file.name.endswith('.xlsx'):
            messages.error(request, 'Please upload a .xlsx file.')
            return redirect('test_name_import_data')

        imported_data = dataset.load(new_file.read(), format='xlsx')

        for data in imported_data:
            test_category_name = data[0]
            test_name = data[1]

            if not test_name or not test_category_name:
                messages.error(request, 'Test name or category name is missing. Skipping this entry.')
                continue

            test_category, created = Test_category.objects.get_or_create(name=test_category_name)

            Test_name.objects.update_or_create(
                name=test_name,
                test_cat_name=test_category,
                defaults={
                    'name': test_name,
                    'test_cat_name': test_category,
                }
            )

        messages.success(request, 'Test names have been imported successfully!')
        return redirect('test_name')

    context = {
        'heading': 'Import Test Names',
    }

    return render(request, 'medicine/test_name.html', context)

@method_decorator(login_required(login_url='login_page'), name='dispatch')
@method_decorator(user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager'])), name='dispatch')
class InstructionCRUDView(View):    
    def get(self, request, *args, **kwargs):
        instruction_id = kwargs.get('id')
        if instruction_id:            
            instruction = get_object_or_404(ConditionInstruction, id=instruction_id)
            instruction_data = {
            'id': instruction.id,
            'instruction': instruction.instruction,
            }
            return JsonResponse(instruction_data, safe=False)
        # Fetch all instruction
        instruction = ConditionInstruction.objects.all().values('id', 'instruction')
        return JsonResponse(list(instruction), safe=False)

    def post(self, request, *args, **kwargs):
        instruction_id = kwargs.get('id')
        if instruction_id:            
            instruction = get_object_or_404(ConditionInstruction, id=instruction_id)
            form = ConditionInstructionForm(request.POST, instance=instruction)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'instruction updated successfully'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        # Create a new instruction
        form = ConditionInstructionForm(request.POST)
        if form.is_valid():
            instruction = form.save(commit=False)
            instruction.created_by = request.user.username
            instruction.save()
            return JsonResponse({'status': 'success', 'message': 'instruction created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        # Delete a instruction
        instruction_id = kwargs.get('id')
        instruction = get_object_or_404(ConditionInstruction, id=instruction_id)
        instruction.delete()
        return JsonResponse({'status': 'success', 'message': 'Instruction deleted successfully'})

@method_decorator(login_required(login_url='login_page'), name='dispatch')
@method_decorator(user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager'])), name='dispatch')
class ProductCRUDView(View):    
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        if product_id:            
            product = get_object_or_404(Brand_name, id=product_id)
            product_data = {
            'id': product.id,
            'item_code': product.item_code,
            'name': product.name,
            'strength': product.strength,
            'category': product.category.id,
            'company': product.pharmaceutical_com_id.id,
            'generic': product.generics_id.id,
            'dosage': product.dosage_form_id.id,
            }
            return JsonResponse(product_data, safe=False)
        # Fetch all product
        products = Brand_name.objects.select_related('category', 'pharmaceutical_com_id', 'generics_id', 'dosage_form_id').values('id','item_code','name','strength','category__name', 'pharmaceutical_com_id__name','generics_id__name','dosage_form_id__name')[:50]
        return JsonResponse(list(products), safe=False)

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        if product_id:            
            product = get_object_or_404(Brand_name, id=product_id)
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'product updated successfully'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        # Create a new product
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user.username
            product.save()
            return JsonResponse({'status': 'success', 'message': 'product created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        # Delete a product
        product_id = kwargs.get('id')
        product = get_object_or_404(Brand_name, id=product_id)
        product.delete()
        return JsonResponse({'status': 'success', 'message': 'product deleted successfully'})


from django.views.decorators.http import require_GET

@require_GET
def autocomplete_medicines(request):
    query = request.GET.get('term', '')  # Adjusted to match 'term' as used in the JavaScript
    if query:
        medicines = Brand_name.objects.filter(name__istartswith=query)[:10]
        results = [{
            'label': f"{m.name} {m.strength} {m.dosage_form_id.name}",
            'value': f"{m.name} {m.strength} {m.dosage_form_id.name}",
            'name': m.name,
            'strength': m.strength,
            'dosage_form': m.dosage_form_id.name
        } for m in medicines]
        
        
    else:
        results = []
    
    return JsonResponse(results, safe=False)

@require_GET
def autocomplete_tests(request):
    query = request.GET.get('query', '')
    tests = Test_name.objects.filter(name__icontains=query)[:10]
    results = [{'label': t.name, 'value': t.name} for t in tests]
    return JsonResponse(results, safe=False)

@require_GET
def autocomplete_condition_instruction(request):
    term = request.GET.get('term', '')  # Get the search term
    instructions = ConditionInstruction.objects.filter(instruction__icontains=term)[:10]  # Filter by 'instruction'
    results = [{'label': t.instruction, 'value': t.instruction} for t in instructions]  # Return label and value
    return JsonResponse(results, safe=False)


@csrf_exempt
@require_POST
def assign_prescription(request):
    doctor_id = request.user
    dosage_form_id=None
    try:
        data = json.loads(request.body)
        pres_user_phone = data.get('user')
        calling_id = data.get('calling_id')
        # Retrieve the CallRecord instance
        try:
            calling_instance = CallRecord.objects.get(id=calling_id)
        except CallRecord.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Call record not found.'})
        
        doctor_Call_serve = Doctor_Call_serve.objects.filter(doctor=doctor_id,call_record=calling_instance).first()
        if not doctor_Call_serve:
            return JsonResponse({'success': False, 'error': 'Doctor call service not found.'})

        call_duration = data.get('call_duration')
        call_duration_update =calling_instance.update_call_duration(call_duration)

        patient_name= data.get('patient_name')
        patient_no= data.get('ppno')
        patient_age= data.get('patient_age')
        patient_gender= data.get('patient_gender')

        medicine_history= data.get('medicine_history')
        risk_factor= data.get('risk_factor')
        problem= data.get('problem')
        advice= data.get('advice', '')
        followup= data.get('followup', None)
   
        medicines = data.get('medicines', [])

        selected_tests_raw = data.get('selected_tests', '')
        if isinstance(selected_tests_raw, str):
            selected_tests = selected_tests_raw.split(',')
        else:
            selected_tests = []

        prescription = Prescription.objects.create(
            patient_name=patient_name,
            patient_phone_no=patient_no, 
            patient_age=patient_age,
            gender=patient_age,
            prescription_req=doctor_Call_serve,
            drug_history=medicine_history,
            risk_factors=risk_factor,
            problem=problem,
            advice=advice,
            follow_up=followup
        )
        
        for med in medicines:
            brand_name = med['medicineName'].strip()
            brand_strength = med['strength'].strip() if med['strength'] else None
            brand_dosage_form = med['dosage_form_name'].strip() if med['dosage_form_name'] else None

            dosage_form_id = Dosage_Form.objects.get(name=brand_dosage_form)

            try:
                if brand_strength is None:
                    brand_name_med = Brand_name.objects.get(name=brand_name, dosage_form_id=dosage_form_id)
                else:
                    brand_name_med = Brand_name.objects.get(name=brand_name, strength=brand_strength, dosage_form_id=dosage_form_id)
            except Brand_name.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'Brand_name with name "{brand_name}", strength "{brand_strength}", and dosage form "{brand_dosage_form}" does not exist.'})

            condition_instruction = None
            conditional_instruction_name = med.get('conditionalInstruction')
            if conditional_instruction_name:
                try:
                    condition_instruction = ConditionInstruction.objects.get(instruction=conditional_instruction_name)
                except ConditionInstruction.DoesNotExist:
                    condition_instruction = None

            PrescriptionItem.objects.create(
                prescription=prescription,
                brand_name=brand_name_med,
                dosage=med['dosage'],
                dosage_instruction=med['dosageInstruction'],
                meal_instructions=med['mealInstruction'],
                condition_instruction=condition_instruction,
                additional_instructions='',
                duration=med['duration']
            )
        
        for test_name in selected_tests:
            test_obj = get_object_or_404(Test_name, name=test_name)
            PrescriptionTestSuggest.objects.create(
                prescription=prescription,
                test_name=test_obj
            )
        doctor_Call_serve.change_status(True)

        doctor_instance = get_object_or_404(Doctor, id=doctor_id.id)
        profile_instance=doctor_instance.doc_profile
        profile_instance.mark_online() 

        return JsonResponse({'success': True, 'prescription_id': prescription.id})
        

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def rejected_prescription(request):
    doctor_id = request.user

    try:
        doctor = Doctor.objects.get(id=doctor_id.id)
        call_record_id = request.POST.get('voiceCallId')
        rejected_reason = request.POST.get('rejection_reason')

        print(doctor,call_record_id,rejected_reason)

        if not call_record_id or not rejected_reason:
            return JsonResponse({'success': False, 'message': 'voiceCallId and rejected reason are required.'})

        doctor_call_instance = Doctor_Call_serve.objects.get(
            doctor=doctor, call_record__id=call_record_id
        )
        
        success = doctor_call_instance.update_rejected_reason(rejected_reason)

        if success:
            return JsonResponse({'success': True, 'message': 'Rejected reason updated successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update rejected reason.'})

    except Doctor_Call_serve.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Call record not found.'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)})


@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager']))
def view_prescription(request):
    doctorPrescripList = Doctor_Call_serve.objects.filter(status=True).order_by('-updated_at') 
    context = {
        'doctorPrescripList':doctorPrescripList,
        'heading': "View Prescription"
    }
    return render(request, 'prescription/view_prescription/view_prescription.html', context)


@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager']))
def get_prescription_data(request, prescription_id):
    dec_req = get_object_or_404(Doctor_Call_serve, id=prescription_id)
    prescriptions = Prescription.objects.filter(prescription_req=dec_req)
     
    if prescriptions.exists():
        prescription = prescriptions.first()
        data = {
            'prescription_id': prescription.id,
            'patient_phone_no': prescription.patient_phone_no,
            'prescription_date': prescription.prescription_date.strftime('%d-%m-%Y'),
            'doctor_name': prescription.doctor.name,
            'doctor_bmdc': prescription.doctor.doc_profile.bmdc_no,
            'doctor_qualification': prescription.doctor.doc_profile.designation,
            'patient_name': prescription.patient_id.patient_phone_no,
            'patient_gender': prescription.patient_id.patient_phone_no,
            'patient_age': prescription.patient_id.patient_phone_no,
            'patient_weight': prescription.patient_id.patient_phone_no,
            'problem': prescription.problem,
            'advice': prescription.advice,
            'medicines': [
                f"{item.brand_name.dosage_form_id.name} {item.brand_name.name}{' - ' + item.brand_name.strength if item.brand_name.strength else ''} &nbsp;&nbsp;&nbsp; {item.dosage} &nbsp;&nbsp;&nbsp; {item.meal_instructions} &nbsp;&nbsp;&nbsp; {item.duration} days"  
                for item in prescription.items.all() 
            ],
            'investigation': ', '.join([test.test_name.name for test in prescription.prescription_tests.all()]),
            'follow_up': prescription.follow_up.strftime('%d-%m-%Y') if prescription.follow_up else ''
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "No Prescription found for this doctor request."}, status=404)


class PrescriptionRequesrView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        group = request.data.get("group")
        ppno = request.data.get("ppno") 
        if group not in ["patient", "pharmacy"]:
            return JsonResponse({'error': 'Invalid group provided'}, status=400)

        user = request.user
        doctor_calls = []

        if group == 'patient':
            if user.groups.filter(name='patient').exists():
                doctor_calls = Doctor_Call_serve.objects.filter(
                    call_record__patient_id=user.id, status=True
                )
            else:
                return JsonResponse({'error': 'Unauthorized group for this user'}, status=403)

        elif group == 'pharmacy':
            if user.groups.filter(name='pharmacy').exists():
                
                doctor_calls = Doctor_Call_serve.objects.filter(
                    call_record__pharmacy_id=user.id,
                    status=True
                )

                if ppno: 
                    doctor_calls = doctor_calls.filter(call_record__ppno=ppno)
            else:
                return JsonResponse({'error': 'Unauthorized group for this user'}, status=403)
        
        data = [{
            'id': call.id,
            'patient_no': call.call_record.ppno,
            'created_at': call.created_at
        } for call in doctor_calls]

        return JsonResponse(data, safe=False)

        
class DownloadPrescriptionPDFView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, prescription_id):
        doctor_call = get_object_or_404(Doctor_Call_serve, id=prescription_id)
        prescription = Prescription.objects.filter(prescription_req=doctor_call).first()
        if not prescription:
            return Response({"error": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)
        watermark_path = "pdf/Shastokotha.png" 
        logo_path = "pdf/logo.png" 
        pdf_content = generate_prescription_pdf(prescription, watermark_path=watermark_path, logo_path=logo_path)
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=prescription_{prescription_id}.pdf'
        
        return response


# class DownloadPrescriptionPDF(LoginRequiredMixin, View):
#     login_url = 'login'

#     def get(self, request, prescription_id):
#         doctor_call = get_object_or_404(Doctor_Call_serve, id=prescription_id)
#         prescription = Prescription.objects.filter(prescription_req=doctor_call).first()
#         if not prescription:
#             raise Http404("Prescription not found")
        
#         watermark_path = "pdf/Shastokotha.png" 
#         logo_path = "pdf/logo.png" 
        
#         pdf_content = generate_prescription_pdf(prescription, watermark_path=watermark_path, logo_path=logo_path)
        
#         response = HttpResponse(pdf_content, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=prescription_{prescription_id}.pdf'
        
#         return response
    

class DownloadPrescriptionPDF(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, prescription_id):
        doctor_call = get_object_or_404(Doctor_Call_serve, id=prescription_id)
        prescription = Prescription.objects.filter(prescription_req=doctor_call).first()
        if not prescription:
            raise Http404("Prescription not found")
        
        watermark_path = "pdf/Shastokotha.png" 
        logo_path = "pdf/logo.png" 
        
        pdf_content = generate_prescription_pdf(prescription, watermark_path=watermark_path, logo_path=logo_path)
        
        response = HttpResponse(pdf_content, content_type='application/pdf')
        # Set content disposition to inline to view in the browser
        response['Content-Disposition'] = f'inline; filename=prescription_{prescription_id}.pdf'
        
        return response
