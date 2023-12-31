from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Patient, PatientMedicalReports, Appointment, ConsultationHistory, PatientMedicalHistory
from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _


def validate_mobile_number(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError('Mobile number must be a 10-digit number.')

def validate_name(value):
    if not re.match(r'^[A-Za-z ]+$', value):
        raise ValidationError('Name must contain only letters and spaces.')

class DoctorSignUpForm(UserCreationForm):

    name = forms.CharField(max_length=255,validators=[validate_name])
    mobile_no = forms.CharField(max_length=10,validators=[validate_mobile_number])
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
    name = forms.CharField(max_length=255,validators=[validate_name])
    mobile_no = forms.CharField(max_length=10,validators=[validate_mobile_number])
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


class PatientDetailsForm(forms.ModelForm):
    name = forms.CharField(max_length=255,validators=[validate_name])
    mobile_no = forms.CharField(max_length=10,validators=[validate_mobile_number])
    address = forms.CharField(widget=forms.Textarea)
    weight = forms.IntegerField()
    height = forms.IntegerField()
    blood_group = forms.ChoiceField(
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')])
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    age = forms.IntegerField()
    class Meta:
        model = Patient
        fields = ['name', 'email', 'mobile_no', 'address',
                  'weight', 'height', 'blood_group', 'gender', 'age']


class MedicalRecordForm(forms.ModelForm):
    def validate_pdf(value):
        if not value.name.lower().endswith('.pdf'):
            raise ValidationError(_('Please upload pdf files only'), code='invalid_file_type')
    medical_report = forms.FileField(validators=[validate_pdf])
    class Meta:
        model = PatientMedicalReports
        fields = ['medical_report_name', 'test_date', 'medical_report']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_report': forms.FileInput()  # Ensure this is included
        }


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = PatientMedicalHistory
        fields = ['allergies', 'prior_diseases', 'family_history']


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].label_from_instance = lambda obj: f"{obj.name}"

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        empty_label="Select Doctor"
    )
    # appointment_date_time = forms.DateTimeField(
    #     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    # )
    appointment_date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'text', 'class': 'form-control datetimepicker', 'placeholder': 'MM/DD/YYYY hh:mm AM/PM'}),
        input_formats=['%m/%d/%Y %I:%M %p']  # Specify the desired format here
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date_time', 'subject']


class ConsultationForm(forms.ModelForm):
    follow_up_date = forms.DateTimeField(
        required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = ConsultationHistory
        fields = ['symptoms', 'diagnosis', 'prescribed_medication',
                  'recommended_lab_tests', 'remarks', 'follow_up_date']
