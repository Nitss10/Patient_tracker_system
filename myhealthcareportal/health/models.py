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