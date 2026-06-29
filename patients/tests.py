from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Patient, ClinicalRecord

# Create your tests here.
class HeartFailureAPITests(APITestCase):

    def setUp(self):
        """
        Set up baseline testing data 
        """
        #Create sample patient matching high-risk factors
        self.high_risk_patient = Patient.objects.create(
            age=65.0, sex=1, smoking=True, diabetes=True, anaemia=False, high_blood_pressure=True
        )
        self.record1 = ClinicalRecord.objects.create(
            patient=self.high_risk_patient,
            creatinine_phosphokinase=250,
            ejection_fraction=25,
            platelets=50000.0,
            serum_creatinine=1.5,
            serum_sodium=130,
            follow_up_days=15,
            death_event=True
        )

        # Create baseline standard patient
        self.normal_patient = Patient.objects.create(
            age=45.0, sex=0, smoking=False, diabetes=False, anaemia=False, high_blood_pressure=False
        )
        self.record2 = ClinicalRecord.objects.create(
            patient=self.normal_patient,
            creatinine_phosphokinase=100,
            ejection_fraction=45,
            platelets=250000.0,    
            serum_creatinine=0.8,
            serum_sodium=140,
            follow_up_days=120,  
            death_event=False
        )

    def test_create_patient_endpoint(self):
        """Test if POST endpoint successfully creates patient"""
        url = reverse('create_patient')
        data = {
            "age": 50.0,
            "sex": 0,
            "smoking": False,
            "diabetes": True,
            "anaemia": True,
            "high_blood_pressure": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 3)

    def test_high_risk_patients_endpoint(self):
        """Test filtering logic for triple-comorbidity patients"""
        url = reverse('high_risk_patients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only find the high_risk patient not normal one
        self.assertEqual(response.data['count'], 1)

    def test_critical_platelets_endpoint(self):
        """Test filtering logic for physiological extremes of platelet counts"""
        url = reverse('critical_platelets')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_survival_stats_aggregation(self):
        """Test for ORM data aggregation success"""
        url = reverse('survival_stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('metrics', response.data)

    def test_patient_medical_history_nested(self):
        """Test that fetching patient returns their historical records nested"""
        url = reverse('patient_history', kwargs={'pk': self.high_risk_patient.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('clinical_records', response.data)
        self.assertEqual(len(response.data['clinical_records']), 1)

    def test_recent_followups_endpoint(self):
        """Test for the filtering boundaries for temporal tracking limits"""
        url = reverse('recent_followups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
