from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime, date, timedelta
import re
from .models import User, Patient, Doctor, Specialist, DoctorAvailability, Appointment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings


class SignupForm(forms.Form):
    first_name = forms.CharField(label="Nombre: ", required=True)
    last_name = forms.CharField(label="Apellido: ", required=True)
    email = forms.EmailField(label="Email: ", required=True)
    password = forms.CharField(label='Password', required=True)
    dni = forms.CharField(label='DNI', required=True)

class RegisterForm(UserCreationForm):
    #birthdate = forms.DateField()
    
    class Meta:
        model = User
        fields = ["email", "password1", "password2",  "first_name", "last_name"]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Password'})

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
        #self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']



    
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')


class ContactoForm(forms.Form):
    first_name = forms.CharField(label="Nombre: ", required=True)
    last_name = forms.CharField(label="Apellido: ", required=True)
    email = forms.EmailField(label="Email: ", required=True)

class PatientForm(forms.ModelForm):
    
    dni = forms.CharField(label='DNI: ', required=True)
    phone = forms.IntegerField(label='Teléfono:')
    address = forms.CharField(label='Domicilio completo:')
    city = forms.CharField(label='Localidad: ')
    social_work = forms.CharField(label='Obra Social:')
    sw_number = forms.CharField(label='Número de afiliado:')
    date_of_birth = forms.DateField(
        initial=date(1990, 1, 1),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'max': (date.today() - timedelta(days=18*365)).strftime('%Y-%m-%d'),
                'min': date(1920, 1, 1).strftime('%Y-%m-%d'),
                
            }
        )
    )
    class Meta:
            model = Patient
            fields = ['dni', 'phone', 'address', 'city', 'social_work', 'sw_number', 'date_of_birth' ]

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError('DNI debe ser un número y contener solo 8 dígitos' )
        return dni
        
    
    def clean_phone(self):
        phone = str(self.cleaned_data['phone'])
        phone = re.sub(r'\D', '', phone)  # remove all non-digit characters
        if len(phone) < 10:
            raise forms.ValidationError('El número de teléfono debe ser al menos de 10 digitos.')
        return phone

    
class SpecialistForm(forms.ModelForm):
    
    class Meta:
        model = Specialist
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        
   
# class DoctorForm(forms.Form): #create Doctor
#     specialist = forms.ModelChoiceField(queryset=Specialist.objects.all())
#     # class Meta:   #voy a especificar q modelo pertenece
#     model = Doctor
#     fields = ['__all__'] #campos a utilizar en este form
#     widgets = {
#         'specialist': forms.Select(attrs={'class': 'form-control'}),
#         'image_profile': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        
            #'title': forms.TextInput(attrs= { 'class': 'form-control', 'placeholder': 'Write a title'}),
            #'description': forms.Textarea(attrs= { 'class': 'form-control', 'placeholder': 'Write a description'}),
            #'important': forms.CheckboxInput(attrs= { 'class': 'form-check-input m-auto'}
        # }
  
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['dni','phone','address','city','mr_number','specialist','image_profile']
        widgets = {
            'specialist': forms.Select(attrs={'class': 'form-control'}),
            'image_profile': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }  
    

    def save(self, commit=True):
        doctor = super().save(commit=False)
        if commit:
            doctor.save()
        return doctor
    # user_form = CustomUserCreationForm()
    # def save(self, commit=True):
    #     instance = super().save(commit=False)

    #     # CustomUserCreationForm
    #     user_form = CustomUserCreationForm(self.data)
    #     if user_form.is_valid():
    #         user = user_form.save(commit=False)
    #         user.is_doctor = True  # Marcar el usuario como médico
    #         user.save()
    #         instance.user = user

    #         if commit:
    #             instance.save()
    #         return instance
    #     else:
    #         # Manejar errores en el formulario de usuario aquí
    #         pass

# class DoctorAvailabilityForm(forms.ModelForm):
#     class Meta:
#         model = DoctorAvailability
#         fields = ['doctor', 'day', 'start_time', 'end_time']

#     def clean(self):
#         cleaned_data = super().clean()
#         doctor = cleaned_data.get('doctor')
#         day = cleaned_data.get('day')
#         start_time = cleaned_data.get('start_time')
#         end_time = cleaned_data.get('end_time')

#         # Check if there is already an availability record for this doctor on this day
#         if DoctorAvailability.objects.filter(doctor=doctor, day=day).exists():
#             raise forms.ValidationError('There is already an availability record for this doctor on this day.')

#         # Check if start_time is earlier than end_time
#         if start_time and end_time and start_time >= end_time:
#             raise forms.ValidationError('Start time must be earlier than end time.')

#         # Check if there is no overlap with other availability records for this doctor
#         overlaps = DoctorAvailability.objects.filter(doctor=doctor, day=day, start_time__lt=end_time, end_time__gt=start_time)
#         if overlaps.exists():
#             raise forms.ValidationError('The availability overlaps with another availability record for this doctor on this day.')

#         return cleaned_data
    





class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['doctor', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ('doctor', 'patient', 'start_time', 'end_time')
#         widgets = {
#             'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }



class AppointmentCreateForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label=None)
    date = forms.DateField(widget=forms.SelectDateWidget)
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'start_time', 'end_time', 'description']

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if doctor and date and start_time and end_time:
            # Check if the selected time slot is available for the selected doctor
            availability = DoctorAvailability.objects.filter(doctor=doctor, date=date)
            if not availability.exists():
                raise forms.ValidationError('Selected time slot is not available for this doctor.')
            else:
                time_slots = []
                for a in availability:
                    start = max(a.start_time, start_time)
                    end = min(a.end_time, end_time)
                    if start < end:
                        time_slots.append((start, end))

                if not time_slots:
                    raise forms.ValidationError('Selected time slot is not available for this doctor.')
                else:
                    self.fields['start_time'].widget = forms.Select(choices=[(t[0], t[0].strftime('%I:%M %p')) for t in time_slots])
                    self.fields['end_time'].widget = forms.Select(choices=[(t[1], t[1].strftime('%I:%M %p')) for t in time_slots])

                    appointment_start = datetime.combine(date, start_time)
                    appointment_end = datetime.combine(date, end_time)
                    conflicting_appointments = Appointment.objects.filter(doctor=doctor, date=date, start_time__lt=appointment_end, end_time__gt=appointment_start)
                    if conflicting_appointments.exists():
                        raise forms.ValidationError('Selected time slot conflicts with an existing appointment.')

        return cleaned_data


### otros ejemplos###
# class AppointmentForm(forms.ModelForm):
#     doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label=None)
#     date = forms.DateField(widget=forms.SelectDateWidget)
#     start_time = forms.ChoiceField(choices=[], widget=forms.Select())
#     end_time = forms.ChoiceField(choices=[], widget=forms.Select())

#     class Meta:
#         model = Appointment
#         fields = ['doctor', 'date', 'start_time', 'end_time', 'description']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['start_time'].choices = []
#         self.fields['end_time'].choices = []

#     def clean(self):
#         cleaned_data = super().clean()
#         start_time = cleaned_data.get('start_time')
#         end_time = cleaned_data.get('end_time')
#         if start_time and end_time and start_time >= end_time:
#             self.add_error('end_time', 'End time must be after start time.')

#     def set_time_choices(self, doctor_availability):
#         time_slots = doctor_availability.get_time_slots()
#         self.fields['start_time'].choices = time_slots
#         self.fields['end_time'].choices = time_slots




# class AppointmentCreateForm(forms.ModelForm):
#     doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label=None)
#     date = forms.DateField(widget=forms.SelectDateWidget)
#     start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
#     end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
#     description = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Appointment
#         fields = ['doctor', 'date', 'start_time', 'end_time', 'description']

#     def clean(self):
#         cleaned_data = super().clean()
#         doctor = cleaned_data.get('doctor')
#         date = cleaned_data.get('date')
#         start_time = cleaned_data.get('start_time')
#         end_time = cleaned_data.get('end_time')

#         if doctor and date and start_time and end_time:
#             # Check if the selected time slot is available for the selected doctor
#             availability = DoctorAvailability.objects.filter(doctor=doctor, date=date, start_time__lte=start_time, end_time__gte=end_time)
#             if not availability.exists():
#                 raise forms.ValidationError('Selected time slot is not available for this doctor.')
#             else:
#                 appointment_start = datetime.combine(date, start_time)
#                 appointment_end = datetime.combine(date, end_time)
#                 conflicting_appointments = Appointment.objects.filter(doctor=doctor, date=date, start_time__lt=appointment_end, end_time__gt=appointment_start)
#                 if conflicting_appointments.exists():
#                     raise forms.ValidationError('Selected time slot conflicts with an existing appointment.')
#         return cleaned_data

# class AppointmentForm(forms.ModelForm):
#     doctor = forms.ModelChoiceField(queryset=DoctorAvailability.objects.all(), empty_label=None)
#     date = forms.DateField(widget=forms.SelectDateWidget)
#     start_time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'))
#     end_time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'))

#     class Meta:
#         model = Appointment
#         fields = ['doctor', 'date', 'start_time', 'end_time', 'description']
