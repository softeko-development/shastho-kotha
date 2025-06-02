from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patient-reports', PatientReportViewSet, basename='patient-reports')
router.register(r'pharmacy-reports', PharmacyReportViewSet, basename='pharmacy-reports')
# router.register(r'users', UserViewSet)
# router.register(r'calls', CallViewSet)

urlpatterns = [
    path('user/staff_list/add_staff/', add_staff ,name='add_staff' ),
    path('user/staff_list/', staff_list ,name='staff_list' ),
    path('user/doctor_list/add_doctor/', add_doctor ,name='add_doctor' ),
    path('user/doctor_list/', doctor_list ,name='doctor_list' ),
    path('user/pharmacy_list/add_pharmacy/', add_pharmacy ,name='add_pharmacy' ),
    path('user/pharmacy_list/', pharmacy_list ,name='pharmacy_list' ),
    path('setting/profile_settings/', profile_settings ,name='profile_settings' ),
    path('setting/site_settings/', site_settings ,name='site_settings' ),
    path('update-working-status/<int:doctor_id>/', update_working_status, name='update_working_status'),
    path('api/user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/register/pharmacy/', PharmacyRegistrationView.as_view(), name='pharmacy-register'),
    path('api/register/doctor/', DoctorRegisterView.as_view(), name='doctor-register'),
    path('api/register/staff/', StaffRegisterView.as_view(), name='staff-register'), 
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/login/otp/', OTPLoginView.as_view(), name='otp-login'),
    path('api/update-fcm-token/', UpdateFCMTokenView.as_view(), name='update-fcm-token'),
    # path('doclist/', include(router.urls)),
    path('change_password/', change_password, name='change_password'),
    
]+ router.urls