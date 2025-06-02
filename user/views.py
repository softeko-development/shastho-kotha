from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from .forms import *
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.decorators import user_passes_test, login_required
from user.decorators import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import update_session_auth_hash
from rest_framework.decorators import action
from django.http import HttpResponse


@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def add_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, request.FILES)
        profile_form = StaffProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            # Create a Teacher instance
            staff = Staff(
                avatar=form.cleaned_data['avatar'],
                username=form.cleaned_data['user_id'],
                phone_number=form.cleaned_data['phone_number'],
                name=form.cleaned_data['name'],
                gender=form.cleaned_data['gender'],
                nid=form.cleaned_data['nid'],
                email=form.cleaned_data['email'],
                user_id=form.cleaned_data['user_id'],
                password=make_password(form.cleaned_data['phone_number'])
            )
            staff.save()

            # Now fetch the created teacher instance
            staff_instance = Staff.objects.get(username=form.cleaned_data['user_id'])

            # Create a TeacherProfile instance with the correct teacher_field
            staff_profile = StaffProfile(
                staff_field=staff_instance,
                designation=profile_form.cleaned_data['designation']
            )
            staff_profile.save()

            messages.success(request, 'Staff data has been Added!')
            return redirect('add_staff')

    else:
        form = StaffRegistrationForm()
        profile_form = StaffProfileForm()

    context = {
        'form': form,
        'profile_form': profile_form,
        'heading': 'Staff',
    }

    return render(request, 'user/staff/add_staff.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def edit_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    staff_profile = staff.teacher_profile

    if request.method == 'POST':
        form = StaffEditRegistrationForm(request.POST,request.FILES, instance=staff)
        profile_form = StaffProfileForm(request.POST, request.FILES, instance=staff_profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Staff data has been Updated ! ! !')
            return redirect('staff_list')
    else:
        form = StaffEditRegistrationForm(instance=staff)
        profile_form = StaffProfileForm(instance=staff_profile)

    context = {
        'form': form,
        'profile_form': profile_form,
        'heading': 'Staff Update',
    }
    return render(request, 'user/staff/edit_staff.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def staff_list(request):
    stafflist=Staff.objects.all()
    context={
        'stafflist':stafflist,
        'heading':'Staff'
    }
    return render(request, 'user/staff/staff.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def del_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    staff.delete()
    messages.success(request, 'Staff data has been Updated ! ! !')
    return redirect(staff_list)


@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        profile_form = DoctorProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            # Create a Teacher instance
            doctor = Doctor(
                avatar=form.cleaned_data['avatar'],
                username=form.cleaned_data['user_id'],
                phone_number=form.cleaned_data['phone_number'],
                name=form.cleaned_data['name'],
                gender=form.cleaned_data['gender'],
                nid=form.cleaned_data['nid'],
                email=form.cleaned_data['email'],
                user_id=form.cleaned_data['user_id'],
                password=make_password(form.cleaned_data['phone_number'])
            )
            doctor.save()

            # Now fetch the created teacher instance
            doctor_instance = Doctor.objects.get(username=form.cleaned_data['user_id'])

            # Create a TeacherProfile instance with the correct teacher_field
            doctor_profile = DoctorProfile(
                doctor_field=doctor_instance,
                specialization=profile_form.cleaned_data['specialization'],
                designation=profile_form.cleaned_data['designation'],
                education=profile_form.cleaned_data['education'],
                cirtification=profile_form.cleaned_data['cirtification'],
                bmdc_no=profile_form.cleaned_data['bmdc_no'],
            )
            doctor_profile.save()

            messages.success(request, 'Doctor data has been Added!')
            return redirect('add_doctor')

    else:
        form = DoctorRegistrationForm()
        profile_form = DoctorProfileForm()

    context = {
        'form': form,
        'profile_form': profile_form,
        'heading': 'Doctor',
    }

    return render(request, 'user/doctor/add_doctor.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor_profile = doctor.doc_profile

    if request.method == 'POST':
        form = DoctorEditRegistrationForm(request.POST,request.FILES, instance=doctor)
        profile_form = DoctorProfileForm(request.POST, request.FILES, instance=doctor_profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Doctor data has been Updated ! ! !')
            return redirect('doctor_list')
    else:
        form = StaffEditRegistrationForm(instance=doctor)
        profile_form = StaffProfileForm(instance=doctor_profile)

    context = {
        'form': form,
        'profile_form': profile_form,
        'heading': 'Doctor Update',
    }
    return render(request, 'user/doctor/edit_doctor.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def doctor_list(request):
    doctorlist=Doctor.objects.all()
    context={
        'doctorlist':doctorlist,
        'heading':'Doctor'
    }
    return render(request, 'user/doctor/doctor.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def del_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    messages.success(request, 'Doctor data has been Deleted ! ! !')
    return redirect(doctor_list)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def add_pharmacy(request):
    if request.method == 'POST':
        form = PharmacyRegistrationForm(request.POST, request.FILES)
        profile_form = PharmacyProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            # Create a Teacher instance
            pharmacy = Pharmacy(
                avatar=form.cleaned_data['avatar'],
                username=form.cleaned_data['user_id'],
                phone_number=form.cleaned_data['phone_number'],
                name=form.cleaned_data['name'],
                gender=form.cleaned_data['gender'],
                nid=form.cleaned_data['nid'],
                email=form.cleaned_data['email'],
                user_id=form.cleaned_data['user_id'],
                password=make_password(form.cleaned_data['phone_number'])
            )
            pharmacy.save()

            # Now fetch the created teacher instance
            pharmacy_instance = Pharmacy.objects.get(username=form.cleaned_data['user_id'])

            # Create a TeacherProfile instance with the correct teacher_field
            pharmacy_profile = PharmacyProfile(
                pharmacy_field=pharmacy_instance,
                cirtification=profile_form.cleaned_data['cirtification'],
                post=profile_form.cleaned_data['post'],
                thana_or_upazila=profile_form.cleaned_data['thana_or_upazila'],
                district=profile_form.cleaned_data['district'],
                division=profile_form.cleaned_data['division'],
            )
            pharmacy_profile.save()

            messages.success(request, 'Pharmacy data has been Added!')
            return redirect('add_pharmacy')

    else:
        form = PharmacyRegistrationForm()
        profile_form = PharmacyProfileForm()

    context = {
        'form': form,
        'profile_form': profile_form,
        'heading': 'Pharmacy',
    }

    return render(request, 'user/pharmacy/add_pharmacy.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def edit_pharmacy(request, id):
    pharmacy = get_object_or_404(Doctor, id=id)
    pharmacy_profile = pharmacy.pharma_profile

    if request.method == 'POST':
        form = PharmacyEditRegistrationForm(request.POST,request.FILES, instance=pharmacy)
        profile_form = PharmacyProfileForm(request.POST, request.FILES, instance=pharmacy_profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Pharmacy data has been Updated ! ! !')
            return redirect('pharmacy_list')
    else:
        form = PharmacyEditRegistrationForm(instance=pharmacy)
        profile_form = PharmacyProfileForm(instance=pharmacy_profile)

    context = {
        'form': form,
        'profile_form': profile_form,
        'heading': 'Pharmacy Update',
    }
    return render(request, 'user/doctor/edit_pharmacy.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def pharmacy_list(request):
    pharmacylist=Pharmacy.objects.filter(status="Active")
    totolPharmacy=pharmacylist.count()
    context={
        'pharmacylist':pharmacylist,
        'totolPharmacy':totolPharmacy,
        'heading':'Pharmacy'
    }
    return render(request, 'user/pharmacy/pharmacy.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def del_pharmacy(request, id):
    pharmacy = get_object_or_404(Pharmacy, id=id)
    pharmacy.delete()
    messages.success(request, 'Pharmacy data has been Deleted ! ! !')
    return redirect(pharmacy_list)


@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def profile_settings(request):
    context = {
        'heading': "Profile Settings"
    }
    return render(request, 'settings/profile_settings.html', context)

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, roles=['Manager', 'HR']))
def site_settings(request):
    context = {
        'heading': "Site Settings"
    }
    return render(request, 'settings/site_settings.html', context)


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        user = self.get_object()

        if hasattr(user, 'pharma_profile'):
            return PharmacySerializer
        elif hasattr(user, 'doc_profile'):
            return DoctorSerializer
        elif hasattr(user, 'staff_profile'):
            return StaffSerializer
        return CustomUserSerializer
    
class PharmacyRegistrationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        user = request.user
        try:
            pharmacy = CustomUser.objects.get(id=user.id)
            serializer = PharmacySerializer(pharmacy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Pharmacy not found for this user'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        user = request.user
        
        try:
            pharmacy = CustomUser.objects.get(id=user.id)
            print('pharmacy', pharmacy)
            serializer = PharmacySerializer(pharmacy, data=request.data, partial=True)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Pharmacy not found for this user'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            pharmacy = serializer.save() 
            return Response({
                'message': 'Pharmacy profile updated successfully',
                'user_id': pharmacy.id
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = DoctorSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class StaffRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = StaffSerializer
    parser_classes = [JSONParser,MultiPartParser, FormParser]
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        login_serializer = self.get_serializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        validated_data = login_serializer.validated_data
        
        response_data = {
            'refresh': validated_data['refresh'],
            'access': validated_data['access'],
            'group': validated_data['group'],
            'user_id': validated_data['user_id'],
        }
        
        fcm_token = request.data.get('fcm_token')
        
        if fcm_token:
            UserDevice.objects.update_or_create(
                user_id=validated_data['user_id'],
                defaults={'fcm_token': fcm_token}
            )
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class OTPLoginView(APIView):
    def post(self, request):
        serializer = OTPLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DoctorViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        status = 'Active'
        # Filter doctors who are active and have a working_status of True in their profile
        doctors = Doctor.objects.filter(status=status, doc_profile__working_status=True)
        serializer = DoctorSerializer(doctors, many=True)
        return Response({'doctors': serializer.data})
    

# from .utils import create_zoom_meeting
# from datetime import datetime, timedelta  

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

  
# class CallViewSet(viewsets.ModelViewSet):
#     queryset = Call.objects.all()
#     serializer_class = CallSerializer

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         caller_id = data.get('caller')
#         receiver_id = data.get('receiver')
        
#         # Retrieve users
#         caller = CustomUser.objects.get(id=caller_id)
#         receiver = CustomUser.objects.get(id=receiver_id)
        
#         # Create Zoom meeting
#         topic = f"Call between {caller.name} and {receiver.name}"
#         start_time = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + 'Z'  # Schedule to start in 5 minutes
#         duration = 30  # 30 minutes
        
#         meeting_info = create_zoom_meeting(topic, start_time, duration)
        
#         # Save Call information
#         call = Call.objects.create(
#             caller=caller,
#             receiver=receiver,
#             status='initiated',
#             start_time=datetime.utcnow(),
#         )
        
#         # Return response with meeting details
#         response_data = {
#             'call_id': call.id,
#             'meeting_url': meeting_info.get('join_url'),
#             'meeting_id': meeting_info.get('id'),
#             'meeting_password': meeting_info.get('password')
#         }
        
#         return Response(response_data, status=status.HTTP_201_CREATED)


@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", roles=['Manager']))
@csrf_exempt 
def update_working_status(request, doctor_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            working_status = data.get('working_status', False)
            doctor_instance = get_object_or_404(Doctor, id=doctor_id)
            profile_instance=doctor_instance.doc_profile
            profile_instance.working_status = working_status
            if working_status == False:
                profile_instance.mark_offline()
            else:
                profile_instance.mark_online()
            profile_instance
            profile_instance.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


class UpdateFCMTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UserDeviceSerializer(data=request.data)
        if serializer.is_valid():
            fcm_token = serializer.validated_data['fcm_token']
            user_device, created = UserDevice.objects.update_or_create(
                user=user,
                defaults={'fcm_token': fcm_token}
            )

            if created:
                message = "FCM token created and saved successfully"
            else:
                message = "FCM token updated successfully"

            return Response({"message": message}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('cpassword')
            if new_password == confirm_password:
                hashed_password = make_password(new_password)
                request.user.password = hashed_password
                request.user.save()
                messages.success(request, 'Your password was successfully updated!')
                update_session_auth_hash(request, request.user)
                return redirect('change_password')
            else:
                messages.error(request, 'The passwords do not match.')
    context={
        'heading': 'User',
        'subheading':'Password Change',
    }
    return render(request,'user/password_change.html',context)


class PatientReportViewSet(viewsets.ModelViewSet):
    serializer_class = PatientReportSerializer
    queryset = PatientReport.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return PatientReport.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        report = self.get_object()
        file_path = report.report_file.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{report.report_name}"'
            return response

class PharmacyReportViewSet(viewsets.ModelViewSet): 
    serializer_class = PharmacyReportSerializer
    queryset = pharmacyReport.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return pharmacyReport.objects.filter(pharmacy_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(pharmacy_id=self.request.user)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        report = self.get_object()
        file_path = report.report_file.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{report.report_name}"'
            return response
