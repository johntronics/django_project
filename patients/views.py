from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from .models import Patient, ClinicalRecord
from .serializers import PatientSerializer, ClinicalRecordSerializer
from django.http import HttpResponse
import sys
import django

#Endpoint 1: Create New Patient (POST endpoint)
@api_view(['POST'])
def create_patient(request):
    """
    Validates and saves a new patient profile into the database.
    """
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Endpoint 2: High Risk Profile Filter (GET endpoint)
@api_view(['GET'])
def high_risk_patients(request):
    """
    Returns patients who are smokers, have diabetes, AND high blood pressure.
    """
    patients = Patient.objects.filter(smoking=True, diabetes=True, high_blood_pressure=True)
    serializer = PatientSerializer(patients, many=True)
    return Response({
        "count": patients.count(),
        "description": "Patients matching triple-comorbidity (Smoking, Diabetes, High Blood Pressure)",
        "results": serializer.data
    })


#Endpoint 3: Critical Platelet Count (GET endpoint)
@api_view(['GET'])
def critical_platelets(request):
    """
    Returns clinical records where platelets are abnormally low (< 150,000) OR high (> 450,000).
    """
    records = ClinicalRecord.objects.filter(platelets__lt=150000) | ClinicalRecord.objects.filter(platelets__gt=450000)
    serializer = ClinicalRecordSerializer(records, many=True)
    return Response({
        "count": records.count(),
        "condition": "Platelets outside normal physiological range (<150k or >450k)",
        "results": serializer.data
    })


#Endpoint 4: Survival Stat Aggregations (GET endpoint)
@api_view(['GET'])
def survival_stats(request):
    """
    Calculates average ejection fractions and sodium levels grouped by survival outcome.
    """
    stats = ClinicalRecord.objects.values('death_event').annotate(
        average_ejection_fraction=Avg('ejection_fraction'),
        average_serum_sodium=Avg('serum_sodium'),
        total_cases=Count('id')
    )
    return Response({
        "description": "Comparative statistical breakdown between living and deceased measurements",
        "metrics": stats
    })


#Endpoint 5: Nested Patient Medical History (GET endpoint)
@api_view(['GET'])
def patient_history(request, pk):
    """
    Relational Nested Query.
    Fetches a specific patient along with all their related historical lab results.
    """
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response({"error": "Patient profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
    serializer = PatientSerializer(patient)
    return Response(serializer.data)


#Endpoint 6: Followup Records (GET endpoint)
@api_view(['GET'])
def recent_followups(request):
    """
    Filters clinical cases monitored for any range up to 30 days.
    """
    records = ClinicalRecord.objects.filter(follow_up_days__lte=30)
    serializer = ClinicalRecordSerializer(records, many=True)
    return Response({
        "count": records.count(),
        "timeframe": "Follow-up period <= 30 days",
        "results": serializer.data
    })

#Landing Page ---
def api_root_view(request):
    """
    Renders the main API documentation page using Django templates.
    Passes system information into the template context.
    """
    context = {
        'python_version': sys.version.split(' ')[0],
        'django_version': django.get_version(),
    }
    return render(request, 'index.html', context)