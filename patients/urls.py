from django.urls import path
from . import views

urlpatterns = [
    path("patients/create/", views.create_patient, name="create_patient"),
    path("patients/high-risk/", views.high_risk_patients, name="high_risk_patients"),
    path("records/critical-platelets/", views.critical_platelets, name="critical_platelets"),
    path("records/survival-stats/", views.survival_stats, name="survival_stats"),
    path("patients/<int:pk>/history/", views.patient_history, name="patient_history"),
    path("records/recent-followups/", views.recent_followups, name="recent_followups"),
]