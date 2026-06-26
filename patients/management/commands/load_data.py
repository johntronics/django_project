import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from patients.models import Patient, ClinicalRecord

class Command(BaseCommand):
    help = 'Bulk loads heart failure clinical records from CSV into the database'

    def handle(self, *args, **kwargs):
        # find the safe path to our data
        csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'heart_failure.csv')
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"File not found at {csv_file_path}"))
            return
        self.stdout.write("Cleaning off old data...")
        Patient.objects.all().delete()

        records_to_create = []

        # Open and read the CSV file
        self.stdout.write("Reading CSV data...")
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Create the Patient object for linking to the Clinical record
                patient = Patient.objects.create(
                    age=float(row['age']),
                    sex=int(row['sex']),
                    smoking=bool(int(row['smoking'])),
                    diabetes=bool(int(row['diabetes'])),
                    anaemia=bool(int(row['anaemia'])),
                    high_blood_pressure=bool(int(row['high_blood_pressure']))
                )

                # Prepare the ClinicalRecord, linking it to the patient i just created
                record = ClinicalRecord(
                    patient=patient,
                    creatinine_phosphokinase=int(row['creatinine_phosphokinase']),
                    ejection_fraction=int(row['ejection_fraction']),
                    platelets=float(row['platelets']),
                    serum_creatinine=float(row['serum_creatinine']),
                    serum_sodium=int(row['serum_sodium']),
                    follow_up_days=int(row['time']),
                    death_event=bool(int(row['DEATH_EVENT']))
                )
                
                # Append to our list instead of saving to the database immediately
                records_to_create.append(record)

        self.stdout.write("Bulk inserting clinical records into the database...")
        ClinicalRecord.objects.bulk_create(records_to_create)

        # Output positive message
        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(records_to_create)} patients and records!"))