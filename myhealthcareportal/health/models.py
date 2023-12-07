from django.db import models
from django.contrib.auth.models import User

# Assuming each user will be associated with either a Doctor or a Patient
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile_no = models.CharField(max_length=255)
    address = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    qualification = models.CharField(max_length=255)
    specialisation = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    bio = models.TextField()
    # hashed_password field is not needed because Django's User model already handles password hashing

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile_no = models.CharField(max_length=255)
    address = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    weight = models.IntegerField()
    height = models.IntegerField()
    blood_group = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.IntegerField()

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date_time = models.DateTimeField()
    subject = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

class PatientMedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    allergies = models.CharField(max_length=255)
    prior_diseases = models.CharField(max_length=255)
    family_history = models.CharField(max_length=255)

class PatientMedicalReports(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medical_report_name = models.CharField(max_length=255)
    test_date = models.DateField()
    medical_report = models.FileField(upload_to='medical_reports/')


class ConsultationHistory(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=255)
    diagnosis = models.CharField(max_length=255)
    prescribed_medication = models.TextField()  # BLOB field is equivalent to Django's TextField
    recommended_lab_tests = models.CharField(max_length=255)
    remarks = models.TextField()
    last_updated_on = models.DateTimeField(auto_now=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
