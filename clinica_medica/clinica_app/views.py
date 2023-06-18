from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactoForm, CustomUserCreationForm, CustomUserChangeForm, LoginForm, PatientForm, DoctorForm, Branch_officeForm, SpecialistForm, DoctorAvailabilityForm, AppointmentCreateForm, AppointmentEditForm, SlotForm
from django.contrib.auth.decorators import login_required
from .models import Patient, Specialist, Doctor, Appointment, DoctorAvailability, Slot, Branch_office
from clinica_app.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate,login,logout
from datetime import datetime, date, timedelta, time
from django.utils import timezone
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.views.generic.list import ListView
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test


def index(request):
    patient_id = None
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user)
            patient_id = patient.id
        except Patient.DoesNotExist:
            # Handle the case where the user is logged in but has no associated patient
            pass
    context = {'patient_id': patient_id}
    print(patient_id)
    return render(request, 'clinica_app/index.html', context)   
    
def services(request):
    context = {}
    return render(request, 'clinica_app/services.html', context)

def staff(request):
    doctors_staff = Doctor.objects.all().order_by('user__last_name')
    specialists = Specialist.objects.all()
    context = {
        'doctors' : doctors_staff,
        'specialists' : specialists
    }
    return render(request, 'clinica_app/staff.html', context)

from datetime import datetime


def about_us(request):
    context = {}
    return render(request, 'clinica_app/about_us.html', context)

def contact(request):
    context = {}
    return render(request, 'clinica_app/contact.html', context)

def contacto(request):
    if request.method == 'POST':
        contacto_form = ContactoForm(request.POST)
    else:
        contacto_form = ContactoForm()
    return render(request, 'clinica_app/contacto.html', {
        'contacto_form': contacto_form
    })

def welcome(request):
    context = {}
    return render(request, 'clinica_app/welcome.html', context)
    
#---------------------------------- PATIENT ----------------------------------
@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            user = request.user
            user.is_patient = True
            user.save()
            messages.success(request,  messages.SUCCESS, 'Paciente dado de alta con exito')
            return redirect('appointment')
    else:
         form = PatientForm()    

    context = {
        'form': form
    }
    return render(request, 'clinica_app/patient/patient_create.html', context)

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, user=request.user)
    
    if not request.user.is_patient:
        raise Http404() 
    else : 
        patient = Patient.objects.get(pk=pk, user=request.user)

    return render(request, 'clinica_app/patient/patient_detail.html', {'patient': patient})

def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        print(form.errors)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            return redirect('patient_detail', pk=patient.id)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'clinica_app/patient/patient_update.html', {'form': form, 'patient': patient})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('patients')

#---------------------------------- SLOTS ----------------------------------

def slot_view(request):
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    specialist_id = request.GET.get('specialist')
    flag= False

    # Obtén todos los turnos
    slots = Slot.objects.all().order_by('date', 'start_time')

    # Aplica los filtros si se proporcionaron valores
    if doctor_id:
        slots = slots.filter(doctor_id=doctor_id)
        flag = True
    if date:
        slots = slots.filter(date=date)
        flag = True
    if specialist_id:
        slots = slots.filter(doctor__specialist_id=specialist_id)
        flag = True
   ##-----------------------  
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)

            # Obtén los datos del formulario
            doctor = form.cleaned_data['doctor']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            
            # Calcula el intervalo de veinte minutos
            interval = timedelta(minutes=20)

            # Crea múltiples registros basados en el intervalo de veinte minutos
            current_datetime = datetime.combine(datetime.today(), start_time)
            end_datetime = datetime.combine(datetime.today(), end_time)
            slots = []

            while current_datetime < end_datetime:
                current_time = current_datetime.time()

                slot = Slot(
                    doctor=slot.doctor,
                    date=slot.date,
                    start_time=current_time,
                    end_time=(current_datetime + interval).time(),
                    # Otros campos relevantes para los registros
                )
                slots.append(slot)
                current_datetime += interval

            Slot.objects.bulk_create(slots)
            slot_list = Slot.objects.filter(doctor=doctor).order_by('date', 'doctor', 'start_time')
            
            return redirect('slot_view')
    else:
        form = DoctorAvailabilityForm() 
   
     # mostrar la slot_list ordenada por fecha y hora
    if flag==False:
        filtered_slots = slots.order_by('date', 'start_time')
       
    else:
        filtered_slots = slots

    specialist_list = Specialist.objects.all()

    # Get the list of doctors based on the selected specialist
    doctor_list = Doctor.objects.all()
    if specialist_id:
        doctor_list = doctor_list.filter(specialist_id=specialist_id)
    context = {
        'form': form,
        'doctor_list': doctor_list,
        'slot_list': filtered_slots,
        'specialist_list': specialist_list,
    }
    return render(request, 'clinica_app/admin/appointments/slots.html', context)

@login_required
def edit_slot(request, pk):
    slot = get_object_or_404(Slot, id=pk)

    if request.method == 'POST':
        form = SlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            return redirect('slot_view')
    else:
        form = SlotForm(instance=slot)

    context = {
        'form': form,
        'doctor_list': Doctor.objects.all(),
        'slot': slot,
    }
    return render(request, 'clinica_app/admin/appointments/edit_slot.html', context)

@login_required
def delete_slot(request, pk):
    slot = get_object_or_404(Slot, id=pk)

    if request.method == 'POST':
        slot.delete()
        return redirect('slot_view')

    context = {
        'slot': slot,
    }
    return render(request, 'clinica_app/admin/appointments/delete_slot.html', context)

#---------------------------------- APPOINTMENT ----------------------------------
@login_required
def appointment(request):
    context = {}
    doctor_id = request.GET.get('doctor')
    specialist_id = request.GET.get('specialist')
    date = request.GET.get('date')

    # Filtra los slots con hora igual o posterior a la hora actual
    slots = Slot.objects.filter(date__gte=datetime.now())

    selected_doctor = None
    
    show_error = False
    if date:
       slots = slots.filter(date=date)
    else:
      date = None    

    if specialist_id:
        slots = slots.filter(doctor__specialist_id=specialist_id)

    specialist_selected = bool(specialist_id)
    if doctor_id:
        if doctor_id != 'None':
            slots = slots.filter(doctor_id=doctor_id)
        
            selected_doctor = Doctor.objects.get(id=doctor_id)
            specialist = selected_doctor.specialist  # Get the specialist of the selected doctor
            date_str = request.GET.get('date')
            
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
              
                has_appointment = request.user.patient.has_appointment_with_doctor(selected_doctor.id)
            else:
                has_appointment = False
        else:
            selected_doctor = None
            specialist = None
            has_appointment = False
    elif specialist_id:
        specialist = Specialist.objects.get(id=specialist_id)
        has_appointment = request.user.patient.has_appointment_with_specialist(specialist)
        selected_doctor = None
    else:
        selected_doctor = None
        specialist = None
        has_appointment = False     

    if request.method == 'POST':
        form = AppointmentCreateForm(request.POST, request=request)
        if form.is_valid():
            start_time = datetime.strptime(request.POST['start_time'], '%H:%M').time()
            end_time = datetime.strptime(request.POST['end_time'], '%H:%M').time()
            form.cleaned_data['start_time'] = start_time
            form.cleaned_data['end_time'] = end_time
            
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient

            slot_id = form.cleaned_data['slot_id']
            slot = Slot.objects.get(id=slot_id, status='available')
            
            if appointment.has_appointment_with_other_doctor():
                error_message = appointment.has_appointment_with_other_doctor()
                messages.error(request, error_message)
                show_error = True
                current_date = timezone.now().date()
                patient = request.user.patient
                appointments = Appointment.objects.filter(patient=patient)
    
                context = {
                    'current_date': current_date,
                    'patient_appointments': appointments,
                    'show_error': show_error,
                }
                return render(request, 'clinica_app/patient_appointments.html', context)
               
            else:
                show_error = False
                
            appointment.slot = slot
            slot.status = 'booked'
            slot.save()
            appointment.save()
            messages.success(request, 'Appointment created successfully.')
            
            return redirect(reverse('appointment_show', kwargs={'pk': appointment.id}))
        else:   
            messages.error(request, 'Failed to create appointment. Please check the form data.')
    else:
        form = AppointmentCreateForm(request=request)
    
    #current_time = datetime.now().time()
    specialist_list = Specialist.objects.all()

    doctor_list = Doctor.objects.all()
    if specialist_id:
        doctor_list = doctor_list.filter(specialist_id=specialist_id)
   
    current_date = timezone.now().date()
    
    #Aca filtra los slots para que se vean solo los que tienen la fecha de hoy en adelante y 
    # si tienen la fecha de hoy que se fije la hora actual

    # COMENTE ESTO PORQUE NO ME DEJABA VER LOS SLOTS DE OTROS DIAS---------------------------------------
    # if current_date in slots.values_list('date', flat=True):
    #     slots = slots.filter(start_time__gte=datetime.now().time()) 
    
    if request.user.is_patient:
        appointments = request.user.patient.appointments.filter(date__gte=current_date)
        has_appointment = appointments.exists()

    date_selected = bool(date)
    stored_messages = request.session.get('appointment_messages', None)
    if stored_messages:
    # Pasar los mensajes almacenados a la plantilla
        context['stored_messages'] = stored_messages
    # Clear the appointment messages from the session before filtering
    if 'appointment_messages' in request.session:
        del request.session['appointment_messages']
    
    # Calcular la fecha de inicio de la semana (lunes)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    # Obtener los días de la semana a partir de hoy

    weekdays = [start_of_week + timedelta(days=i) for i in range(30)]
    
    # sorted_slots = sorted(slots, key=lambda slot: slot.start_time)

     # Generar lista de horas
    start_hour = time(8, 0)  # Hora de inicio
    end_hour = time(20, 0)  # Hora de fin
    interval = 20  # Intervalo de minutos
    hours = []
    current_hour = start_hour

    if date is None:
        date = datetime.now().date()  # Asignar fecha actual si date es None

    while current_hour <= end_hour:
        hours.append(current_hour.strftime('%H:%M'))
        current_hour = (datetime.combine(datetime.strptime(str(date), '%Y-%m-%d').date(), current_hour) + timedelta(minutes=interval)).time()

        # current_hour = (datetime.combine(date.today(), current_hour) + timedelta(minutes=interval)).time()

    weekdays_length = len(weekdays) + 1  # Obtener la longitud de weekdays y sumar 1
    
    context = {
        'form': form,
        'doctor_list': doctor_list,
        'specialist_list': specialist_list,
        'slot_list': slots,
        'doctor_selected': doctor_id,
        'specialist_selected': specialist_selected,
        'current_date': current_date,
        'has_appointment': has_appointment,
        'selected_doctor': selected_doctor,
        'specialist': specialist,
        'date_selected': date_selected,
        'stored_messages': stored_messages,
        'show_error': show_error,
        'has_appointment': has_appointment, 
        'weekdays': weekdays,
        'hours': hours,
        'weekdays_length': weekdays_length,
    }
    return render(request, 'clinica_app/appointment.html', context)

def appointment_show(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'clinica_app/appointment_show.html', {'appointment': appointment})

def appointment_list(request):
    appointments = Appointment.objects.all().order_by('date', 'start_time')
    context = {'appointments': appointments}
    return render(request, 'clinica_app/appointments/appointment_list.html', context)

def patient_appointments(request):
    current_date = timezone.now().date()
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient)
    
    context = {
        'current_date': current_date,
        'patient_appointments': appointments
    } 
    return render(request, 'clinica_app/patient_appointments.html', context)

def appointment_create(request):
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    specialist_id = request.GET.get('specialist')
    # Filter the slots based on the selected doctor or date
    slots = Slot.objects.all()
    slots = slots.filter(date__gte=datetime.now()) # Filtrar slots con fecha igual o posterior a hoy
    print(slots)
    if doctor_id:
        slots = slots.filter(doctor_id=doctor_id)
    if date:
        slots = slots.filter(date=date)
    if specialist_id:
        slots = slots.filter(doctor__specialist_id=specialist_id)

    # Now you can access the associated specialist for each slot
    
    doctor_selec = bool(doctor_id)
    date_selected = bool(date)
    specialist_selected = bool(specialist_id)
    if request.method == 'POST':
        form = AppointmentCreateForm(request.POST, request=request)
        if form.is_valid():
            
             # Convert the start_time and end_time to datetime.time objects
            start_time = datetime.strptime(request.POST['start_time'], '%H:%M').time()
            end_time = datetime.strptime(request.POST['end_time'], '%H:%M').time()
            # Assign the converted time values back to the form cleaned_data
            form.cleaned_data['start_time'] = start_time
            form.cleaned_data['end_time'] = end_time
            #form.save()
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient

            # Check if the selected slot is still available
            slot_id = form.cleaned_data['slot_id']
            try:
                slot = Slot.objects.get(id=slot_id, status='available')
                appointment.slot = slot
                slot.status = 'booked'
                slot.save()
                appointment.save()
                messages.success(request, 'Appointment created successfully.')
                return redirect(reverse('appointment_detail', kwargs={'pk': appointment.id}))

            except Slot.DoesNotExist:
                messages.error(request, 'The selected slot is no longer available.')
        else:
            messages.error(request, 'Failed to create appointment. Please check the form data.')
    else:
        form = AppointmentCreateForm(request=request)
    # Get the list of specialists
    specialist_list = Specialist.objects.all()

    # Get the list of doctors based on the selected specialist
    doctor_list = Doctor.objects.all()
    if specialist_id:
        doctor_list = doctor_list.filter(specialist_id=specialist_id)
    current_date = timezone.now().date()  
    doctor_selected = request.GET.get('doctor')
    context = {
        'form': form,
        'doctor_list': doctor_list,
        'specialist_list': specialist_list,
        'slot_list': slots,
        'doctor_selec': doctor_selec,
        'doctor_selected': doctor_selected,
        'date_selected': date_selected,
        'specialist_selected': specialist_selected,
        'current_date': current_date,
    }
    return render(request, 'clinica_app/appointments/appointment_create.html', context)

def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentEditForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_detail', pk=pk)
    else:
        form = AppointmentEditForm(instance=appointment)
    return render(request, 'clinica_app/appointments/appointment_edit.html', {'form': form})

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'clinica_app/appointments/appointment_detail.html', {'appointment': appointment})

@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.user != appointment.patient.user:
        raise Http404()

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('appointment_list')

    context = {
        'appointment': appointment,
    }
    return render(request, 'clinica_app/appointments/cancel_appointment.html', context)

#---------------------------------- ADMIN ----------------------------------

def home_admin(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    specialists = Specialist.objects.all()
    branch_offices = Branch_office.objects.all()

    isadmin = True
    context = {
        'specialists': specialists,
        'doctors' : doctors,
        'patients': patients,
        'isadmin': isadmin,
        'branch_offices':branch_offices
    }
    return render(request, 'clinica_app/admin/home_admin.html', context)

def login_admin(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_admin')
                   
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'clinica_app/admin/login.html', context)

#---------------------------------- ADM APPOINTMENTS ----------------------------------

def doctors_consults(request):
    appointments = Appointment.objects.all()
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    patient_id = request.GET.get('patient')
    doctor = None
    flag= False

        
    # Aplica los filtros si se proporcionaron valores
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)
        doctor = Doctor.objects.get(id=doctor_id)  # Recupera el objeto Doctor según el ID
        flag = True
    if patient_id:
        appointments = appointments.filter(patient_id=patient_id)
        flag = True
    if date:
        appointments = appointments.filter(date=date)
        flag = True
    # mostrar la slot_list ordenada por fecha y hora
    if flag==False:
        filtered_appointments = appointments.order_by('date', 'start_time')
    
    else:
        filtered_appointments = appointments

    context = {
        'appointments': filtered_appointments,
        'doctors': doctors,
        'patients': patients,
        'doctor': doctor,
        'doctor_id': doctor_id,
        'patient_id': patient_id, 
        'date': date
    }
    return render(request, 'clinica_app/admin/appointments/doctors_consults.html', context)

def patients_consults(request):
    appointments = Appointment.objects.all()
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    patient_id = request.GET.get('patient')
    patient = None
    flag= False

    
    # Aplica los filtros si se proporcionaron valores
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)
        flag = True
    if patient_id:
        appointments = appointments.filter(patient_id=patient_id)
        patient = Patient.objects.get(id=patient_id)  # Recupera el objeto Patient según el ID
        flag = True
    if date:
        appointments = appointments.filter(date=date)
        flag = True
     # mostrar la slot_list ordenada por fecha y hora
    if flag==False:
        filtered_appointments = appointments.order_by('date', 'start_time')
       
    else:
        filtered_appointments = appointments

    context = {
        'appointments': filtered_appointments,
        'doctors': doctors,
        'patients': patients,
        'patient': patient,
        'doctor_id': doctor_id,
        'patient_id': patient_id, 
        'date': date
    }
    return render(request, 'clinica_app/admin/appointments/patients_consults.html', context)




#---------------------------------- BRANCH OFFICES ----------------------------------
def branch_offices(request):
    branch_offices = Branch_office.objects.all()
    return render(request, 'clinica_app/admin/branch_offices.html', {
        'branch_offices': branch_offices
    })

@permission_required('clinica_app.can_view_branch_office')
def branch_office_detail(request, pk):
    branch_office = Branch_office.objects.get(pk=pk)
    return render(request, 'clinica_app/admin/branch_office_detail.html', {'branch_office': branch_office})

def branch_office_delete(request, pk):
    branch_office = Branch_office.objects.get(id=pk)
    if request.method == 'POST':
        branch_office.delete()
        return redirect('branch_offices')
    context = {
        'branch_office': branch_office
    } 
    return render(request, 'clinica_app/admin/branch_office_delete.html', context)   

def branch_office_create(request):
    
    if request.method == 'POST':
        branch_office_form = Branch_officeForm(request.POST, request.FILES)
        if branch_office_form.is_valid():
            branch_office = branch_office_form.save(commit=False)
            branch_office.save()
            return redirect(reverse('branch_offices'))
        else:
            print(branch_office_form.errors)
            
    else:
        branch_office_form = Branch_officeForm()
        
    context = {
        'branch_office_form': branch_office_form
    }    
    return render(request, 'clinica_app/admin/branch_office_create.html', context)

@permission_required('clinica_app.can_change_branch_office')
def branch_office_update(request, pk):
    branch_office = Branch_office.objects.get(id=pk)
    if request.method == 'POST':
        form = Branch_officeForm(request.POST, request.FILES, instance=branch_office)
        if form.is_valid():
            form.save()
            return redirect('branch_offices')
    else:
        form = Branch_officeForm(instance=branch_office)
    context = {
        'form': form,
        'branch_office': branch_office
    }    
    return render(request, 'clinica_app/admin/branch_office_update.html', context)

#---------------------------------- PATIENT ADMIN ----------------------------------
def patients(request):
    patients = Patient.objects.all()
    return render(request, 'clinica_app/admin/patients.html', {
        'patients': patients
    })

def patient_create_admin(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        form = PatientForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_patient = True
            user.save()
            patient = form.save(commit=False)
            patient.user = user
            patient.save()
            
            messages.success(request,  messages.SUCCESS, 'Paciente dado de alta con exito')
            return redirect('patients')
        else:
            print(form.errors)
    else:
         form = PatientForm()    
         user_form = CustomUserCreationForm()
    context = {
        'form': form,
        'user_form': user_form
    }
    return render(request, 'clinica_app/admin/patient_create.html', context)
def patient_update_admin(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            # form.save()
            return redirect('patients')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'clinica_app/admin/patient_update.html', {'form': form, 'patient': patient})

#---------------------------------- SPECIALIST ----------------------------------
class SpecialistsListView(ListView):
    model = Specialist
    context_object_name = 'specialists'
    template_name = 'clinica_app/admin/specialist_list.html'
    ordering = ['name']

def specialist_detail(request, pk):
    specialist = Specialist.objects.get(pk=pk)
    return render(request, 'clinica_app/admin/specialist_detail.html', {'specialist': specialist})

def specialist_delete(request, pk):
    specialist = Specialist.objects.get(id=pk)
    if request.method == 'POST':
        specialist.delete()
        return redirect('specialist_list')
    context = {
        'specialist': specialist
    } 
    return render(request, 'clinica_app/admin/specialist_delete.html', context)   

def specialist_create(request):
    if request.method == 'POST':
        form = SpecialistForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Specialist.objects.create(name=name)
            return redirect(reverse('specialist_list'))
    else:
        form = SpecialistForm()
    context = {
        'form': form
    }
    return render(request, 'clinica_app/admin/specialist_create.html', context)

def specialist_update(request, pk):
    specialist = Specialist.objects.get(id=pk)
    if request.method == 'POST':
        form = SpecialistForm(request.POST)
        if form.is_valid():
            specialist.name = form.cleaned_data['name']
            specialist.save()
            return redirect('specialist_list')
    else:
        form = SpecialistForm(initial={'name': specialist.name})
    context = {
        'form': form,
        'specialist': specialist
    }    
    return render(request, 'clinica_app/admin/specialist_update.html', context)
    
#---------------------------------- DOCTORS ---------------------------------- 
def doctors(request):
    doctors = Doctor.objects.all()
 
    branch_offices = {}
 
    for doctor in doctors:
        branch_offices[doctor] = doctor.branch_offices.all()
        print(branch_offices[doctor])
    return render(request, 'clinica_app/admin/doctors.html', {
        'doctors': doctors,
        'branch_office': branch_offices
    })


@login_required(login_url='/clinica_app/log_in')
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, user=request.user)
    context = {
        'doctor': doctor,
    }
    return render(request, 'clinica_app/doctor_detail.html', context)
def doctor_delete(request, pk):
    doctor = Doctor.objects.get(id=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctors')
    context = {
        'doctor': doctor
    } 
    return render(request, 'clinica_app/admin/doctor_delete.html', context)   


def doctor_create(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        # form = DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.is_doctor = True
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect(reverse('doctors'))
        else:
            print(doctor_form.errors)
            print(user_form.errors)
    else:
        doctor_form = DoctorForm()
        user_form = CustomUserCreationForm()

    context = {
        'user_form': user_form,
        'doctor_form': doctor_form
    }    
    return render(request, 'clinica_app/admin/doctor_create.html', context)


def doctor_update(request, pk):
    doctor = Doctor.objects.get(id=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctors')
    else:
        form = DoctorForm(instance=doctor)
    context = {
        'form': form,
        'doctor': doctor
    }    
    return render(request, 'clinica_app/admin/doctor_update.html', context)


@login_required
def doctor_appointments(request):
    if request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)  # Obtener el doctor actual
        appointments = doctor.appointment_set.all()  # Obtener los turnos del doctor
         # Filtrar turnos por fecha si se proporciona un valor en la URL
        date = request.GET.get('date')
        if date:
            appointments = appointments.filter(date=date)
        context = {
            'doctor': doctor,
            'appointments': appointments
        }

        return render(request, 'clinica_app/doctor_appointments.html', context)
    else:
        return redirect('log_in')
#---------------------------------- LOGIN y demas en uso ----------------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            if user.is_admin == True:
                return redirect(reverse('home_admin'))
            else:
                return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'clinica_app/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    return render(request, 'clinica_app/profile.html', {'user': user})

def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'clinica_app/profile_update.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_admin or user.is_superuser or request.GET.get('admin') == 'True':
                    return redirect(reverse('home_admin'))
                else:
                    return redirect('welcome')
            else:
                form.add_error(None, 'Invalid email or password')
    else:  
        form = LoginForm()

    context = {
        'form': form,
        'form': form,     
    }
    return render(request, 'clinica_app/login1.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')


