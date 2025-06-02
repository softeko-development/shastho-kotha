from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('medicine/product/', product ,name='product' ),
    path('brand_name_import_data/', brand_name_import_data ,name='brand_name_import_data' ),
    path('medicine/category/', category ,name='category' ),
    path('medicine/test_category/', test_category ,name='test_category' ),
    path('medicine/test_name/', test_name ,name='test_name' ),
    path('medicine/test_name_import_data/', test_name_import_data ,name='test_name_import_data' ),
    path('medicine/menufacturer/', menufacturer ,name='menufacturer' ),
    # path('medicine/generics/', generics ,name='generics' ),
    path('medicine/dosage_form/', dosage_form ,name='dosage_form' ),
    
    path('assign_prescription/', assign_prescription, name='assign_prescription'),
    path('prescription/patients_list/', patients_list ,name='patients_list' ),
    path('prescription/view_prescription/', view_prescription, name='view_prescription' ),
    path('prescription/add_instruction/', add_instruction, name='add_instruction' ),    
    path('get-prescription-data/<int:prescription_id>/', get_prescription_data, name='get_prescription_data'),
    path('api/companies/', PharmaceuticalCompaniesCRUDView.as_view(), name='companies_crud'),
    path('api/companies/<int:id>/', PharmaceuticalCompaniesCRUDView.as_view(), name='companies_crud_detail'),
    path('api/generics/', GenericsCRUDView.as_view(), name='generics_crud'),
    path('api/generics/<int:id>/', GenericsCRUDView.as_view(), name='generics_crud_detail'),
    path('api/dosages/', Dosage_FormCRUDView.as_view(), name='dosage_crud'),
    path('api/dosages/<int:id>/', Dosage_FormCRUDView.as_view(), name='dosage_crud_detail'),
    path('api/categories/', MedCategoryCRUDView.as_view(), name='category_crud'),
    path('api/categories/<int:id>/', MedCategoryCRUDView.as_view(), name='category_crud_detail'),
    path('api/test-categories/', TestCategoryCRUDView.as_view(), name='testCategory_crud'),
    path('api/test-categories/<int:id>/', TestCategoryCRUDView.as_view(), name='testCategory_crud_detail'),
    path('api/test-names/', TestNameCRUDView.as_view(), name='testName_crud'),
    path('api/test-names/<int:id>/', TestNameCRUDView.as_view(), name='testName_crud_detail'),
    path('api/instructions/', InstructionCRUDView.as_view(), name='instruction_crud'),
    path('api/instructions/<int:id>/', InstructionCRUDView.as_view(), name='instruction_crud_detail'),
    path('api/products/', ProductCRUDView.as_view(), name='product_crud'),
    path('api/products/<int:id>/', ProductCRUDView.as_view(), name='product_crud_detail'),
    path('api/prescription/pdf/<int:prescription_id>/', DownloadPrescriptionPDFView.as_view(), name='download_prescription_pdf'),
    path('api/prescriptiondownload/pdf/<int:prescription_id>/', DownloadPrescriptionPDF.as_view(), name='download_prescription'), 
    path('api/prescription-requests/', PrescriptionRequesrView.as_view(), name='prescription-requests/'),
    path('rejected_prescription', rejected_prescription, name='rejected_prescription'),
    path('autocomplete/medicines/', autocomplete_medicines, name='autocomplete_medicines'),
    path('autocomplete/condition_instruction/', autocomplete_condition_instruction, name='autocomplete_condition_instruction'),
    path('autocomplete/tests/', autocomplete_tests, name='autocomplete_tests'),
    
]+ router.urls