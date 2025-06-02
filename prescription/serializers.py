from rest_framework import serializers
from .models import *

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPatient
        fields = ['id', 'patient_name', 'patient_phone_no', 'patient_age']



class PharmaceuticalCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmaceutical_Companies
        fields = '__all__'
        
        
class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ['brand_name', 'dosage', 'duration', 'meal_instructions', 'condition_instruction', 'additional_instructions']

class PrescriptionTestSuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionTestSuggest
        fields = ['test_name']

class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)
    prescription_tests = PrescriptionTestSuggestSerializer(many=True, read_only=True)
    medicines = serializers.SerializerMethodField()
    investigation = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = [
            'id', 'patient_id', 'doctor', 'pharmacy_id', 'prescription_date',
            'notes', 'problem', 'advice', 'follow_up', 'items', 'prescription_tests',
            'medicines', 'investigation'
        ]

    def get_medicines(self, obj):
        # Generating the custom 'medicines' field
        return [
            f"{item.brand_name.dosage_form_id.name} {item.brand_name.name} {item.dosage} s{item.meal_instructions} {item.duration}"
            for item in obj.items.all()
        ]

    def get_investigation(self, obj):
        # Generating the custom 'investigation' field
        return ', '.join([test.test_name.name for test in obj.prescription_tests.all()])
    
