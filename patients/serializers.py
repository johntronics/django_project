from rest_framework import serializers
from .models import Patient, ClinicalRecord

class ClinicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalRecord
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    # to automatically includes a patient clinical records in their JSON profile
    clinical_records = ClinicalRecordSerializer(many=True, read_only=True)
    sex_display = serializers.CharField(source='get_sex_display', read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'