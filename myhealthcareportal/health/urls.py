from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication views
    path('', views.home, name='home'),  # Home view
    path('login/', views.login_view, name='login'),  # Login view
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('signup/', views.signup_view, name='signup'),  # Signup view

    # Patient-specific views
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),  # Patient dashboard
    path('patient/update_details/', views.update_patient_details, name='update_patient_details'),  # Update personal details
    path('patient/upload_record/', views.upload_medical_record, name='upload_medical_record'),  # Upload medical record
    path('patient/medical_history/', views.view_medical_history, name='view_medical_history'),  # View medical history
    path('patient/medical_reports/', views.view_medical_reports, name='view_medical_reports'),  
]
