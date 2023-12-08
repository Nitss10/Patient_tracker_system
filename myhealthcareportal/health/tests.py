from django.test import TestCase
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment, ConsultationHistory
from .forms import DoctorSignUpForm, PatientSignUpForm, AppointmentForm, ConsultationForm
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

class DoctorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user for the doctor
        user = User.objects.create_user(username='testdoctor', password='12test12', email='doctor@example.com')
        Doctor.objects.create(user=user, name='Doctor Test', email='doctor@example.com', mobile_no='1234567890', address='123 Test St', qualification='MD', specialisation='Cardiology', gender='M')

    def test_doctor_creation(self):
        doctor = Doctor.objects.get(id=1)
        self.assertTrue(isinstance(doctor, Doctor))

class PatientModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user for the patient
        user = User.objects.create_user(username='testpatient', password='patient12', email='patient@example.com')
        Patient.objects.create(user=user, name='Patient Test', email='patient@example.com', mobile_no='0987654321', address='321 Test Ave', weight=70, height=170, blood_group='A+', gender='F', age=30)

    def test_patient_creation(self):
        patient = Patient.objects.get(id=1)
        self.assertTrue(isinstance(patient, Patient))

class AppointmentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a doctor and patient
        doctor_user = User.objects.create_user(username='testdoctor', password='12test12', email='doctor@example.com')
        patient_user = User.objects.create_user(username='testpatient', password='patient12', email='patient@example.com')
        doctor = Doctor.objects.create(user=doctor_user, name='Doctor Test', email='doctor@example.com', mobile_no='1234567890', address='123 Test St', qualification='MD', specialisation='Cardiology', gender='M')
        patient = Patient.objects.create(user=patient_user, name='Patient Test', email='patient@example.com', mobile_no='0987654321', address='321 Test Ave', weight=70, height=170, blood_group='A+', gender='F', age=30)
        Appointment.objects.create(patient=patient, doctor=doctor, appointment_date_time=timezone.now() + timedelta(days=1), subject='Routine Checkup', completed=False)

    def test_appointment_creation(self):
        appointment = Appointment.objects.get(id=1)
        self.assertTrue(isinstance(appointment, Appointment))
        self.assertEqual(appointment.subject, 'Routine Checkup')

class ConsultationHistoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a doctor, patient, and appointment
        doctor_user = User.objects.create_user(username='testdoctor', password='12test12', email='doctor@example.com')
        patient_user = User.objects.create_user(username='testpatient', password='patient12', email='patient@example.com')
        doctor = Doctor.objects.create(user=doctor_user, name='Doctor Test', email='doctor@example.com', mobile_no='1234567890', address='123 Test St', qualification='MD', specialisation='Cardiology', gender='M')
        patient = Patient.objects.create(user=patient_user, name='Patient Test', email='patient@example.com', mobile_no='0987654321', address='321 Test Ave', weight=70, height=170, blood_group='A+', gender='F', age=30)
        appointment = Appointment.objects.create(patient=patient, doctor=doctor, appointment_date_time=timezone.now() + timedelta(days=1), subject='Routine Checkup', completed=False)
        ConsultationHistory.objects.create(appointment=appointment, symptoms='Coughing', diagnosis='Common Cold', prescribed_medication='Rest and hydration', recommended_lab_tests='None', remarks='Follow up if symptoms persist')

    def test_consultation_creation(self):
        consultation = ConsultationHistory.objects.get(id=1)
        self.assertTrue(isinstance(consultation, ConsultationHistory))
        self.assertEqual(consultation.diagnosis, 'Common Cold')

class AppointmentTests(TestCase):
    
    def setUp(self):
        # Create test user, doctor, and patient
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.doctor = Doctor.objects.create(user=self.user, name='Dr. Test', email='drtest@example.com', mobile_no='1234567890', address='123 Test St', qualification='MD', specialisation='Cardiology', gender='M')
        self.patient = Patient.objects.create(user=self.user, name='Patient Test', email='patienttest@example.com', mobile_no='1234567891', address='321 Test Ave', weight=70, height=170, blood_group='A+', gender='F', age=30)

    def test_appointment_within_working_hours(self):
        # Create an appointment within working hours
        appointment_time = timezone.datetime(2023, 1, 1, 11, 0, 0)  # 11 AM
        Appointment.objects.create(patient=self.patient, doctor=self.doctor, appointment_date_time=appointment_time, subject='Checkup')

        # Attempt to create a conflicting appointment
        conflicting_time = timezone.datetime(2023, 1, 1, 11, 15, 0)  # 11:15 AM
        conflicting_appointment = Appointment(patient=self.patient, doctor=self.doctor, appointment_date_time=conflicting_time, subject='Follow-up')

        # Attempt to create an appointment outside working hours
        outside_hours_time = timezone.datetime(2023, 1, 1, 9, 0, 0)  # 9 AM
        outside_hours_appointment = Appointment(patient=self.patient, doctor=self.doctor, appointment_date_time=outside_hours_time, subject='Early Appointment')

        # Check if the appointments are valid
        self.assertFalse(conflicting_appointment.save())  # This should fail due to a time conflict
        self.assertFalse(outside_hours_appointment.save())  # This should fail due to being outside working hours

class ScheduleAppointmentTestCase(TestCase):
    
    def setUp(self):
        # Create test users for doctor and patient
        doctor_user = User.objects.create_user(username='doc', password='123')
        patient_user = User.objects.create_user(username='pat', password='123')

        self.doctor = Doctor.objects.create(user=doctor_user, name='Dr. Test', email='drtest@example.com', mobile_no='1234567890', address='123 Test St', qualification='MD', specialisation='Cardiology', gender='M')
        self.patient = Patient.objects.create(user=patient_user, name='Patient Test', email='patienttest@example.com', mobile_no='1234567891', address='321 Test Ave', weight=70, height=170, blood_group='A+', gender='F', age=30)

        # Create an appointment for testing
        appointment_time = timezone.now().replace(hour=11, minute=0, second=0, microsecond=0)
        Appointment.objects.create(doctor=self.doctor, patient=self.patient, appointment_date_time=appointment_time, subject="test")

    def test_appointment_within_working_hours(self):
        # Test that an appointment can be created within working hours
        form_data = {
            'doctor': self.doctor.id,
            'patient': self.patient.id,
            'appointment_date_time': timezone.now().replace(hour=10, minute=30),
            'subject': 'test subject'
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_overlapping_appointments(self):
        # Test that overlapping appointments cannot be created
        overlapping_time = timezone.now().replace(hour=11, minute=15)
        form_data = {
            'doctor': self.doctor.id,
            'patient': self.patient.id,
            'appointment_date_time': overlapping_time,
            'subject': 'test subject'
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

class PatientDashboardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='patientuser', password='12345')
        self.patient = Patient.objects.create(user=self.user, name='Patient Test', email='patienttest@example.com', mobile_no='1234567891', address='321 Test Ave', weight=70, height=170, blood_group='A+', gender='F', age=30)

    def test_patient_dashboard_access(self):
        self.client.login(username='patientuser', password='12345')
        response = self.client.get(reverse('patient_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_dashboard.html')




class HomeViewTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')