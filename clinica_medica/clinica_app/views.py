from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactoForm, CustomUserCreationForm, CustomUserChangeForm, LoginForm, PatientForm, DoctorForm, SpecialistForm, DoctorAvailabilityForm, AppointmentCreateForm, AppointmentEditForm, SlotForm
from django.contrib.auth.decorators import login_required
from .models import Patient, Specialist, Doctor, Appointment, DoctorAvailability, Slot
from clinica_app.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate,login,logout
from datetime import datetime, date, timedelta, time
from django.utils import timezone
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.db.models import F, ExpressionWrapper, DurationField
# Create your views here.

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
    #doctors_staff = Doctor.objects.all()
    specialists = Specialist.objects.all()
    
    context = {
        'doctors' : doctors_staff,
        'specialists' : specialists
    }
    return render(request, 'clinica_app/staff.html', context)

def appointment(request):
    context = {}
    return render(request, 'clinica_app/appointment.html', context)

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


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, user=request.user)
    
    return render(request, 'clinica_app/patient/patient_detail.html', {'patient': patient})


def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        print(form.errors)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            #form.save()
            return redirect('patient_detail', pk=patient.id)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'clinica_app/patient/patient_update.html', {'form': form, 'patient': patient})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('patients')


### Turnos ####


def appointment_list(request):
    appointments = Appointment.objects.all().order_by('date', 'start_time')
    context = {'appointments': appointments}
    return render(request, 'clinica_app/appointments/appointment_list.html', context)


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

### Slots###


def slot_view(request):
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
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
        # slots = Slot.objects.all().order_by('date', 'start_time')
    else:
        filtered_slots = slots

    # slot_list = Slot.objects.all()

    context = {
        'form': form,
        'doctor_list': Doctor.objects.all(),
        'slot_list': filtered_slots,
    }
    return render(request, 'clinica_app/admin/appointments/slots.html', context)
### ultimo ap_create ###

def appointment_create(request):
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')

    # Filter the slots based on the selected doctor or date
    slots = Slot.objects.all()
    # filtrar los slot con fecha mayor a la actual
    # slots = slots.filter(date__gte=date.today())
    #otra opcion me muestra error con esa
    slots = slots.filter(date__gte=datetime.now())


    if doctor_id:
        slots = slots.filter(doctor_id=doctor_id)
    
    if date:
        slots = slots.filter(date=date)
    doctor_selected = bool(doctor_id)
    date_selected = bool(date)
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
            print(form.errors)
            messages.error(request, 'Failed to create appointment. Please check the form data.')
    else:
        form = AppointmentCreateForm(request=request)

    context = {
        'form': form,
        'doctor_list': Doctor.objects.all(),
        'slot_list': slots,
        'doctor_selected': doctor_selected,
        'date_selected': date_selected,
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



###Admin ###


def home_admin(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    specialists = Specialist.objects.all()
    isadmin = True
    context = {
        'specialists': specialists,
        'doctors' : doctors,
        'patients': patients,
        'isadmin': isadmin,
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

## Patients ##
#Chequear porque me muestra usuarios
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

## Specialist ##
@login_required
def specialist_list(request):
    specialists = Specialist.objects.all()
    return render(request, 'clinica_app/admin/specialist_list.html', {'specialists': specialists})

def specialist_detail(request, pk):
    specialist = Specialist.objects.get(pk=pk)
    #specialist = get_object_or_404(Specialist, pk=pk)
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
    
## doctors ##   
def doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinica_app/admin/doctors.html', {
        'doctors': doctors
    })

def doctor_detail(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    #specialist = get_object_or_404(Specialist, pk=pk)
    return render(request, 'clinica_app/admin/doctor_detail.html', {'doctor': doctor})

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



######### LOGIN y demas en uso

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
    }

    return render(request, 'clinica_app/login1.html', context)

def logout_view(request):
    # isadmin = False
    # if request.user.is_admin == True:
    #     isadmin = True
       
    logout(request)
    # if isadmin == True:
    #     return redirect(reverse('home_admin'))  
    # else:
    return redirect('index')



