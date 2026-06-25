from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [(0, 'Female'), (1, 'Male')]
    
    age = models.FloatField(help_text="Age of the patient (years)")
    sex = models.IntegerField(choices=GENDER_CHOICES)
    smoking = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    anaemia = models.BooleanField(default=False, help_text="Decrease of red blood cells or hemoglobin")
    high_blood_pressure = models.BooleanField(default=False)

    def __str__(self):
        return f"Patient {self.id} - Age: {self.age}, Sex: {self.get_sex_display()}"
class ClinicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='clinical_records')
    
    # Lab Results
    creatinine_phosphokinase = models.IntegerField(help_text="Level of the CPK enzyme in the blood (mcg/L)")
    ejection_fraction = models.IntegerField(help_text="Percentage of blood leaving the heart at each contraction")
    platelets = models.FloatField(help_text="Platelets in the blood (kiloplatelets/mL)")
    serum_creatinine = models.FloatField(help_text="Level of serum creatinine in the blood (mg/dL)")
    serum_sodium = models.IntegerField(help_text="Level of serum sodium in the blood (mEq/L)")
    
    # Outcomes
    follow_up_days = models.IntegerField(help_text="Follow-up period (days)", db_column='time')
    death_event = models.BooleanField(default=False, help_text="If the patient deceased during the follow-up period")

    def __str__(self):
        return f"Record for Patient {self.patient.id} - Survived: {not self.death_event}"