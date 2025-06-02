from rest_framework import serializers
from .models import CustomUser, PharmacyProfile, DoctorProfile, StaffProfile,UserDevice,Pharmacy,IPatient,PatientReport,pharmacyReport
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
import random
from datetime import timedelta
from telmed.sms import send_sms

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone_number', 'name', 'avatar', 'gender', 'email', 'nid', 'user_id', 'password','status']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(CustomUserSerializer, self).create(validated_data)


class PharmacyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyProfile
        fields = ['cirtification', 'post', 'thana_or_upazila', 'district', 'division']

class PharmacySerializer(serializers.ModelSerializer):
    pharma_profile = PharmacyProfileSerializer()
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'avatar', 'nid', 'pharma_profile']

    def create(self, validated_data):
        
        pharma_profile_data = validated_data.pop('pharma_profile', None)
        user = CustomUser.objects.create(**validated_data)
        if pharma_profile_data:
            PharmacyProfile.objects.create(pharmacy_field=user, **pharma_profile_data)
        group, created = Group.objects.get_or_create(name='pharmacy')
        user.groups.add(group)

        return user

    def update(self, instance, validated_data):
        
        instance.name = validated_data.get('name', instance.name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.nid = validated_data.get('nid', instance.nid)
        instance.save()
        pharma_profile_data = validated_data.get('pharma_profile', None)

        if pharma_profile_data:
            
            profile, created = PharmacyProfile.objects.get_or_create(pharmacy_field=instance)
            
            for key, value in pharma_profile_data.items():
                setattr(profile, key, value)
            profile.save()

        return instance

class DoctorSerializer(CustomUserSerializer):
    doc_profile = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ['doc_profile']

    def get_doc_profile(self, obj):
        profile = DoctorProfile.objects.filter(doctor_field=obj).first()
        if profile:
            return {
                'specialization': profile.specialization,
                'education': profile.education,
                'designation': profile.designation,
                'cirtification': serializers.ImageField().to_representation(profile.cirtification),
                'bmdc_no': profile.bmdc_no,
            }
        return None

    def create(self, validated_data):
        validated_data['status'] = CustomUser.Status.DEACTIVE
        user = super(DoctorSerializer, self).create(validated_data)
        group, created = Group.objects.get_or_create(name='doctor')
        user.groups.add(group)
        return user

class StaffSerializer(CustomUserSerializer):
    staff_profile = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ['staff_profile']

    def get_staff_profile(self, obj):
        profile = StaffProfile.objects.filter(staff_field=obj).first()
        if profile:
            return {
                'designation': profile.designation,
                'role': profile.role,
            }
        return None
    
    def create(self, validated_data):
        validated_data['status'] = CustomUser.Status.DEACTIVE
        user = super(StaffSerializer, self).create(validated_data)
        group, created = Group.objects.get_or_create(name='staff')
        user.groups.add(group)
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    group = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        
        if user.status != CustomUser.Status.ACTIVE:  # Check if the user's status is not ACTIVE
            raise serializers.ValidationError("Your account is not active. Please contact support.")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'group': user.groups.first().name if user.groups.exists() else None,
            'user_id': user.id,
        }
        
def get_or_create_user(phone_number, group_name):
    user = None
    group = Group.objects.get(name=group_name) 
    
    if group_name == 'pharmacy':
        try:
            user = Pharmacy.objects.get(phone_number=phone_number)
        except Pharmacy.DoesNotExist:
            pass
    elif group_name == 'ipatient':
        try:
            user = IPatient.objects.get(phone_number=phone_number)
        except IPatient.DoesNotExist:
            pass
    
    if not user:
        if group_name == 'pharmacy':
            user = Pharmacy.objects.create(phone_number=phone_number)
        elif group_name == 'ipatient':
            user = IPatient.objects.create(phone_number=phone_number)
        
        # Assign the user to the correct group
        user.groups.add(group)
        user.save()
    
    return user


class OTPManager:
    @staticmethod
    def generate_otp():
        otp = random.randint(1000, 9999)
        return str(otp)
    
    @staticmethod
    def send_otp(user):
        otp = OTPManager.generate_otp()
        user.otp = otp
        user.otp_expiry = timezone.now() + timedelta(minutes=5)
        user.save()
        message = f"Your Shastokotha OTP is {otp}"
        send_sms(user.phone_number, message)

class OTPLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(required=False)
    group = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp', None) 
        group = data.get('group')
        user = get_or_create_user(phone_number, group)

        if otp:
            if user.otp != otp:
                raise serializers.ValidationError('Invalid OTP')
            if timezone.now() > user.otp_expiry:
                raise serializers.ValidationError('OTP expired')
            
            user.otp = None
            user.otp_expiry = None
            user.save()

            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'phone_number': user.phone_number,
                'group': group,
            }

        OTPManager.send_otp(user)

        return {
            'message': 'OTP sent to your phone number',
            'phone_number': phone_number,
            'group': group,
        }

        
class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['fcm_token']

    def validate_fcm_token(self, value):
        if not value:
            raise serializers.ValidationError("FCM token cannot be empty.")
        return value

class PatientReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientReport
        fields = ['id', 'patient', 'report_file', 'report_name', 'created_at']

class PharmacyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = pharmacyReport
        fields = ['id', 'pharmacy_id', 'report_file', 'patient_mobile', 'report_name', 'created_at']
        read_only_fields = ['id', 'created_at', 'pharmacy_id']