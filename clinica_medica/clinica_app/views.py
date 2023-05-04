from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import ContactoForm, RegisterForm, CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, AuthenticationForm, LoginForm, PatientForm, DoctorForm, SpecialistForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView



from .models import Patient, Specialist, Doctor
from clinica_app.models import User
#probando autenticacion
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

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
    # patient_id = None
    # if request.user.is_authenticated:
    #     patient = request.user.patient # Assumes a one-to-one relationship between User and Patient models
    #     patient_id = patient.id
    # context = {'patient_id': patient_id}

    # if request.user:

    #     if request.user.is_patient == True:
    #          patient = Patient.objects.get(user=request.user)
       
    #          print(patient)    
    #          context = {'patient': patient, }
    
    

def services(request):
    context = {}
    return render(request, 'clinica_app/services.html', context)

def staff(request):
    doctors_staff = [
        {
            'name': 'Maria',
            'last_name': 'Sanchez',
            'speciality': 'Dermatologia',
        },
         {
            'name': 'Ramiro',
            'last_name': 'Perez',
            'speciality': 'Traumatologia',
        },
         {
            'name': 'Josefina',
            'last_name': 'Correa',
            'speciality': 'Ginecologia',
        },
         {
            'name': 'Carlos',
            'last_name': 'Torres',
            'speciality': 'Cirugia',
        },
         {
            'name': 'Pedro',
            'last_name': 'Lopez',
            'speciality': 'Gastroenterologia',
        },
    ]
    context = {
        'doctors' : doctors_staff
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
# def welcome(request):
#     context = {}
#     return render(request, 'clinica_app/welcome.html', context)
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
            messages.success(request,  messages.SUCCESS, 'Patient created successfully.')
            #messages.add_message(request, messages.SUCCESS, 'Paciente dado de alta con exito', extra_tags="tag1")
            #ver de mandar el patient_id a appointment
            return redirect('appointment')
            
    else:
         form = PatientForm()    

    context = {
        'form': form
    }
    return render(request, 'clinica_app/patient/patient_create.html', context)

def patients(request):
    #patients = Patient.objects.select_related('user').all()
    patients = Patient.objects.all()
    return render(request, 'clinica_app/patient/patients.html', {
        'patients': patients
    })
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, user=request.user)
    
    return render(request, 'clinica_app/patient/patient_detail.html', {'patient': patient})

@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            print(form)
            form.save()
            #investigar como mod. fields del user name y last
            return redirect('patient_detail', pk=patient.patient_id)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'clinica_app/patient/patient_update.html', {'form': form, 'patient': patient})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('patients')


###Admin ###
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
    #patients = Patient.objects.select_related('user').all()
    doctors = Patient.objects.all()
    return render(request, 'clinica_app/admin/doctors.html', {
        'doctors': doctors
    })





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
    logout(request)
    return redirect('index')

@login_required
def custom_logout(request):
    logout(request)
    return redirect('index') # replace 'home' with the name of your home view






##### ADMIN ####
## sin uso por el momento chequear
# def log_in(request):
#     context = {}
#     return render(request, 'clinica_app/login.html', context)


# def signup(request):
#     if request.method == 'POST':
#         signup_form = RegisterForm(request.POST)
#         print(request.POST)
#         if signup_form.is_valid:
#            signup_form.save()
           
#            return HttpResponseRedirect("/thanks/")
       
#     else:
#         signup_form = RegisterForm()

#     context = {
#         'signup_form' : signup_form
#     }
   
#     return render(request, 'clinica_app/signup.html', context)

# def signin(request):
#     context = {}
#     if request.method == "POST":
#         email = request.POST['email']
#         password=request.POST['password']
#         user=authenticate(request,email=email,password=password)
#         if user is not None:
#             login(request,user)
#             return redirect("welcome")
#         else:
#             return render(request,'clinica_app/signin.html',{
#                 "message":"Invalid Credentials"
#             })
#     #return render(request,"userlogin.html")
#     return render(request, 'clinica_app/signin.html', context)

# def signout(request):
#     logout(request)
#     return render(request,'clinica_app/signin.html',{
#         'message':"Logged out"
#     })

# #sin uso

# def patient_edit(request, patient_id):
#     patient = get_object_or_404(Patient, pk=patient_id)
#     if request.method == 'POST':
#         form = PatientForm(request.POST, instance=patient)
#         if form.is_valid():
#             form.save()
#             return redirect('patient_detail', patient_id=patient.id)
#     else:
#         form = PatientForm(instance=patient)
#     return render(request, 'clinica_app/patient/edit.html', {'form': form, 'patient': patient})

# def patient_delete(request, patient_id):
#     patient = get_object_or_404(Patient, pk=patient_id)
#     patient.delete()
#     return redirect('patients')

# @login_required
# def signout(request):
#     logout(request)
#     return redirect('home')


# def signin(request):
#     if request.method == 'GET':
#         return render(request, 'login.html', {
#             'form': AuthenticationForm
#         })
#     else:
#         # autentica usario y password
#         user = authenticate(
#             request, username=request.POST['username'], password=request.POST['password'])
#         # print(request.POST)
#         if user is None:  # usuario no valido
#             return render(request, 'login.html', {
#                 'form': AuthenticationForm,
#                 'error': 'Username or password is incorrect'
#             })
#         else:  # ususario y password correctos
#             login(request, user)  # guardo sesion user
#             return redirect('tasks')

