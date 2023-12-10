from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication views
    path('', views.home, name='home'),  # Home view
    path('login/', views.login_view, name='login'),  # Login view
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('signup/', views.signup_view, name='signup'),  # Signup view
    path('download/<str:filename>/', views.download_file, name='download_file'), # File download

    # Patient-specific views
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),  # Patient dashboard
    path('patient/update_details/', views.update_patient_details, name='update_patient_details'),  # Update personal details
    path('patient/upload_record/', views.upload_medical_record, name='upload_medical_record'),  # Upload medical record
    path('patient/schedule_appointment/', views.schedule_appointment, name='schedule_appointment'),  # Schedule an appointment
    path('patient/view_appointments/', views.view_appointments, name='view_appointments'),  # View appointments
    path('patient/medical_history/', views.view_medical_history, name='view_medical_history'),  # View medical history
    path('patient/medical_reports/', views.view_medical_reports, name='view_medical_reports'),  


    # Doctor-specific views
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # Doctor dashboard
    path('doctor/appointment/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('doctor/delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('doctor/patients/', views.view_patient_list, name='view_patient_list'),  # View patient list
    path('doctor/patient/<int:patient_id>/', views.view_patient_details, name='view_patient_details'),  # View patient details
    path('doctor/patient/<int:patient_id>/add_consultation/', views.add_patient_consultation, name='add_patient_consultation'),  # Add consultation
    path('doctor/appointments/', views.view_appointment_calendar, name='view_appointment_calendar'),  # View appointment calendar
]
