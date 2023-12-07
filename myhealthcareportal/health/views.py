from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Appointment, PatientMedicalHistory, PatientMedicalReports, ConsultationHistory
from django.utils import timezone
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib import messages
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from django.db import IntegrityError 
from .forms import * 
import pytz

# Change timezone here
currentTimeZone = pytz.timezone('US/Eastern')

def home(request):
    # Logic to determine if the user is a doctor or patient can be implemented here
    # For now, it simply renders the home template.
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully logged in.")
            if hasattr(user, 'doctor'):
                return redirect('doctor_dashboard')
            elif hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            else:
                return redirect('home')  # or some other appropriate page
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('home')

from django.contrib import messages
from django.db import IntegrityError

def signup_view(request):
    # Initialize the forms outside of the if-else block
    doctor_form = DoctorSignUpForm(prefix="doctor")
    patient_form = PatientSignUpForm(prefix="patient")

    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'doctor':
            doctor_form = DoctorSignUpForm(request.POST, request.FILES, prefix="doctor")
            if doctor_form.is_valid():
                user = doctor_form.save()
                try:
                    Doctor.objects.create(
                        user=user,
                        name=doctor_form.cleaned_data.get('name'),
                        email=user.email,
                        mobile_no=doctor_form.cleaned_data.get('mobile_no'),
                        address=doctor_form.cleaned_data.get('address'),
                        qualification=doctor_form.cleaned_data.get('qualification'),
                        specialisation=doctor_form.cleaned_data.get('specialisation'),
                        gender=doctor_form.cleaned_data.get('gender'),
                        bio=doctor_form.cleaned_data.get('bio'),
                    )
                    auth_login(request, user)
                    messages.success(request, "Successfully created doctor profile")
                    return redirect('doctor_dashboard')
                except IntegrityError:
                    messages.error(request, "A doctor with the same information already exists.")
            else:
                messages.error(request, doctor_form.errors)
        elif role == 'patient':
            patient_form = PatientSignUpForm(request.POST, request.FILES, prefix="patient")
            if patient_form.is_valid():
                user = patient_form.save()
                try:
                    Patient.objects.create(
                        user=user,
                        name=patient_form.cleaned_data.get('name'),
                        email=user.email,
                        mobile_no=patient_form.cleaned_data.get('mobile_no'),
                        address=patient_form.cleaned_data.get('address'),
                        weight=patient_form.cleaned_data.get('weight'),
                        height=patient_form.cleaned_data.get('height'),
                        blood_group=patient_form.cleaned_data.get('blood_group'),
                        gender=patient_form.cleaned_data.get('gender'),
                        age=patient_form.cleaned_data.get('age'),
                    )
                    auth_login(request, user)
                    messages.success(request, "Successfully created patient profile")
                    return redirect('patient_dashboard')
                except IntegrityError:
                    messages.error(request, "A patient with the same information already exists.")
            else:
                messages.error(request, patient_form.errors)

    return render(request, 'signup.html', {'doctor_form': doctor_form, 'patient_form': patient_form})



# Patient-specific views
@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "Patient profile not found.")
        return redirect('home')

    patient_email = request.user.email
    context = {'patient': patient, 'patient_email': patient_email}
    return render(request, 'patient_dashboard.html', context)



@login_required
def update_patient_details(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "Patient profile not found.")
        return redirect('home')

    if request.method == 'POST':
        form = PatientDetailsForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient details updated successfully.")
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Error updating patient details.")
    else:
        form = PatientDetailsForm(instance=patient)

    return render(request, 'update_patient_details.html', {'form': form})


@login_required
def upload_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = request.user.patient
            # No need to read file content; just save the form
            medical_record.save()
            messages.success(request, "Medical record added")
            return redirect('patient_dashboard')
    else:
        form = MedicalRecordForm()

    return render(request, 'upload_medical_record.html', {'form': form})

@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            proposed_time = form.cleaned_data['appointment_date_time']
            # The 30-minute window before and after the proposed time
            start_window = proposed_time - timezone.timedelta(minutes=30)
            end_window = proposed_time + timezone.timedelta(minutes=30)

            # Check if the proposed time is within the doctor's working hours (10 AM to 5 PM)
            working_hours_start = proposed_time.replace(hour=10, minute=0, second=0, microsecond=0)
            working_hours_end = proposed_time.replace(hour=17, minute=0, second=0, microsecond=0)

            if (proposed_time.replace(tzinfo=None) < timezone.localtime(timezone=currentTimeZone).replace(tzinfo=None)):
                messages.error(request, "Time cannot be in the past")
                return render(request, 'schedule_appointment.html', {'form': form})

            if not (working_hours_start <= proposed_time < working_hours_end):
                messages.error(request, "Doctors are only available between 10 AM to 5 PM.")
                return render(request, 'schedule_appointment.html', {'form': form})

            # Check for overlapping appointments
            overlapping_appointments = Appointment.objects.filter(
                doctor=form.cleaned_data['doctor'],
                appointment_date_time__range=(start_window, end_window)
            )

            if overlapping_appointments.exists():
                messages.error(request, "The appointment time conflicts with an existing appointment.")
                return render(request, 'schedule_appointment.html', {'form': form})

            # No overlapping appointments and within working hours, proceed to save the new appointment
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient  # Assuming the patient is the current user
            appointment.save()
            messages.success(request, "Appointment scheduled successfully.")
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'schedule_appointment.html', {'form': form})

@login_required
def view_appointments(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        # Redirect or show an error if the patient is not found
        return redirect('home')

    # Fetch appointments for the logged-in patient with their consultation history
    appointments = Appointment.objects.filter(patient=patient).prefetch_related('consultationhistory_set')

    timezone.activate(currentTimeZone)
    # Get localtime in the timezone set above which is then used to filter the appointments
    now = timezone.localtime(timezone.now())

    # Separate upcoming and past appointments
    upcoming_appointments = appointments.filter(appointment_date_time__gte=now, completed=0).order_by('appointment_date_time')
    past_appointments = appointments.filter(appointment_date_time__lt=now).order_by('-appointment_date_time') | appointments.filter(completed=1).order_by('-appointment_date_time')

    # Now you can access the consultation history for each appointment in the template

    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments
    }

    return render(request, 'view_appointments.html', context)



@login_required
def view_medical_history(request):
    patient = request.user.patient

    # Handle adding new medical history
    if request.method == 'POST' and 'add' in request.POST:
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            new_history = form.save(commit=False)
            new_history.patient = patient
            new_history.save()
            return redirect('view_medical_history')

    # Display existing medical history
    medical_history = PatientMedicalHistory.objects.filter(patient=patient)
    add_form = MedicalHistoryForm()  # For adding new history

    context = {
        'medical_history': medical_history,
        'add_form': add_form
    }
    return render(request, 'view_medical_history.html', context)


@login_required
def view_medical_reports(request):
    # Check if the logged-in user is a patient
    if not hasattr(request.user, 'patient'):
        messages.error(request, "Access denied. You are not registered as a patient.")
        return redirect('home')

    patient = request.user.patient
    medical_reports = PatientMedicalReports.objects.filter(patient=patient)

    # Add a success message if medical reports are found
    if medical_reports:
        messages.success(request, "Successfully retrieved medical reports.")
    else:
        messages.info(request, "You currently have no medical reports available.")

    context = {
        'medical_reports': medical_reports,
        'patient': patient,
    }
    return render(request, 'view_medical_reports.html', context)

# Doctor-specific views

@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    # Change timezone here and in view_appointments
    timezone.activate(currentTimeZone)

    # Default time range is today
    start_date = timezone.now().date()
    end_date = start_date

    # Update time range based on user input
    if 'time_range' in request.GET:
        time_range = request.GET['time_range']
        if time_range == 'week':
            start_date = start_date - timezone.timedelta(days=start_date.weekday())
            end_date = start_date + timezone.timedelta(days=6)
        elif time_range == 'month':
            start_date = start_date.replace(day=1)
            end_date = (start_date + timezone.timedelta(days=31)).replace(day=1) - timezone.timedelta(days=1)
        elif time_range == 'custom' and 'custom_start' in request.GET and 'custom_end' in request.GET:
            start_date = timezone.datetime.strptime(request.GET['custom_start'], '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(request.GET['custom_end'], '%Y-%m-%d').date()

    # Get appointments within the specified date range
    appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date_time__range=(
            timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time())),
            timezone.make_aware(timezone.datetime.combine(end_date, timezone.datetime.max.time()))
        )
    ).order_by('appointment_date_time')

    # Top X appointments
    if 'top_x' in request.GET:
        try:
            top_x = int(request.GET['top_x'])
            appointments = appointments[:top_x]
        except ValueError:
            pass  # Ignore if the input is not a valid integer

    # Handle marking appointments as completed
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        if appointment_id:
            appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=doctor)
            appointment.completed = True  # Marking the appointment as completed
            appointment.save()
            messages.success(request, "Appointment marked as completed.")
            return redirect('doctor_dashboard')

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'doctor_dashboard.html', context)


@login_required
def view_patient_list(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('home')

    keyword = request.GET.get('keyword', '')
    appointments = Appointment.objects.filter(doctor=doctor)

    if keyword:
        patients_with_history = PatientMedicalHistory.objects.filter(
            Q(allergies__icontains=keyword) |
            Q(prior_diseases__icontains=keyword) |
            Q(family_history__icontains=keyword)
        ).values_list('patient', flat=True)

        patients_with_reports = PatientMedicalReports.objects.filter(
            medical_report_name__icontains=keyword
        ).values_list('patient', flat=True)

        patients_with_consultations = ConsultationHistory.objects.filter(
            Q(symptoms__icontains=keyword) |
            Q(diagnosis__icontains=keyword) |
            Q(prescribed_medication__icontains=keyword) |
            Q(recommended_lab_tests__icontains=keyword) |
            Q(remarks__icontains=keyword)
        ).values_list('appointment__patient', flat=True)

        patient_ids_consultation = set(list(patients_with_consultations))
        patient_ids = set(list(patients_with_history) + list(patients_with_reports) + list(patient_ids_consultation))
        appointments = appointments.filter(patient__id__in=patient_ids)

    patients = {appointment.patient for appointment in appointments}
    context = {'patients': patients, 'keyword': keyword}
    return render(request, 'view_patient_list.html', context)




@login_required
def view_patient_details(request, patient_id):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    patient = get_object_or_404(Patient, pk=patient_id)
    appointments_with_consultations = Appointment.objects.filter(patient=patient).order_by('-appointment_date_time').prefetch_related('consultationhistory_set')
    medical_history = PatientMedicalHistory.objects.filter(patient=patient)
    medical_reports = PatientMedicalReports.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'appointments_with_consultations': appointments_with_consultations,
        'medical_history': medical_history,
        'medical_reports': medical_reports,
    }
    return render(request, 'view_patient_details.html', context)

@login_required
def add_patient_consultation(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    # Get appointment_id from the query parameters
    appointment_id = request.GET.get('appointment_id')
    appointment = get_object_or_404(Appointment, pk=appointment_id, patient=patient)

    if request.method == 'POST':
        if 'mark_done' in request.POST:
            appointment_id = request.POST.get('appointment_id')
            appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=request.user.doctor)
            appointment.completed = True
            appointment.save()
            messages.success(request, "Successfully added consultation")
            return redirect('view_patient_details', patient_id=patient_id)

    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.appointment = appointment  # Link the consultation to the appointment
            follow_up_date = form.cleaned_data.get('follow_up_date')
            consultation.save()

            # Handle follow-up appointment creation logic...
            if follow_up_date:
                Appointment.objects.create(
                    patient=patient,
                    doctor=request.user.doctor,
                    appointment_date_time=follow_up_date,
                    subject=f"{appointment.subject} - Follow-up for : {consultation.symptoms}",
                    completed=False
                )

            return redirect('doctor_dashboard')
    else:
        form = ConsultationForm()

    return render(request, 'add_patient_consultation.html', {'form': form, 'patient': patient, 'appointment': appointment})


@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=request.user.doctor)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully.")
            referrer = request.GET.get('referrer', 'patient_details')
            if referrer == 'dashboard':
                return redirect('doctor_dashboard')
            else:
                return redirect('view_patient_details', patient_id=appointment.patient.id)
    
    else:
        form = AppointmentForm(instance=appointment)

    context = {'form': form, 'appointment': appointment}
    return render(request, 'edit_appointment.html', context)

@login_required
def delete_appointment(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=request.user.doctor)
        patient_id = appointment.patient.id
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
        referrer = request.GET.get('referrer', 'patient_details')
        if referrer == 'dashboard':
            return redirect('doctor_dashboard')
        else:
            return redirect('view_patient_details', patient_id=patient_id)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('home')




@login_required
def view_appointment_calendar(request):
    dates = Appointment.objects.annotate(date=TruncDate(
        'appointment_date_time')).values('date').annotate(c=Count('id'))

    appointments = {date['date']: Appointment.objects.filter(
        appointment_date_time__date=date['date']) for date in dates}

    context = {'appointments': appointments}

    return render(request, 'calendar.html', context)
