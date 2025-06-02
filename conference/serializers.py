from rest_framework import serializers

class GenerateAgoraTokenSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField(required=True)
    doctor_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_patient_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid patient ID.")
        return value

    def validate_doctor_id(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Invalid doctor ID.")
        return value