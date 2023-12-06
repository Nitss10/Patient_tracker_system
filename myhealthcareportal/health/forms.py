from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Patient, PatientMedicalReports, Appointment, ConsultationHistory, PatientMedicalHistory


class DoctorSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    mobile_no = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    qualification = forms.ChoiceField(choices=[
        ("MBBS", "MBBS"),  # Bachelor of Medicine, Bachelor of Surgery
        ("BDS", "BDS"),  # Bachelor of Dental Surgery
        ("BAMS", "BAMS"),  # Bachelor of Ayurvedic Medicine and Surgery
        ("BHMS", "BHMS"),  # Bachelor of Homeopathic Medicine and Surgery
        ("BUMS", "BUMS"),  # Bachelor of Unani Medicine and Surgery
        ("BVSc", "BVSc"),  # Bachelor of Veterinary Science
        ("MD", "MD"),  # Doctor of Medicine
        ("MS", "MS"),  # Master of Surgery
        ("DNB", "DNB"),  # Diplomate of National Board
        ("DM", "DM"),  # Doctorate of Medicine
        ("MCh", "MCh"),  # Master of Chirurgiae
    ]
    )
    specialisation = forms.CharField(max_length=255)
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'mobile_no',
                  'address', 'qualification', 'specialisation', 'gender', 'bio')


class PatientSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    mobile_no = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    weight = forms.IntegerField()
    height = forms.IntegerField()
    blood_group = forms.ChoiceField(
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')])
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'mobile_no',
                  'address', 'weight', 'height', 'blood_group', 'gender', 'age')