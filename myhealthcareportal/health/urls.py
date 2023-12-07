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

    # Doctor-specific views
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # Doctor dashboard

]
