from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime, date, timedelta
import re
from .models import User, Patient, Doctor, Specialist, DoctorAvailability, Appointment, Slot , Branch_office
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError

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

class ContactForm(forms.Form):
    sender = forms.CharField(label="Nombre: ", required=True)
    email = forms.EmailField(label="Email: ", required=True)
    message = forms.CharField(label="Mensaje:", widget=forms.Textarea, required=True)

    def send_email(self):
        sender = self.cleaned_data['sender']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        subject = 'Nuevo mensaje de contacto'
        body = f"Remitente: {sender}\nEmail: {email}\nMensaje: {message}"
        from_email = settings.EMAIL_HOST_USER
        to_email = [settings.EMAIL_HOST_USER]  # Puedes configurar la dirección de correo electrónico de destino

        try:
            send_mail(subject, body, from_email, to_email, fail_silently=False)
            return True  # El correo se envió exitosamente
        except BadHeaderError as e:
            print(e)  # Opcional: muestra el error en la consola para depuración
            return False  # Hubo un error al enviar el correo

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
  
class DoctorForm(forms.ModelForm):
    branch_offices = forms.ModelMultipleChoiceField(
        queryset=Branch_office.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    
    class Meta:
        model = Doctor
        fields = ['dni','phone','address','city','mr_number','specialist','image_profile','branch_offices']
        widgets = {
            'specialist': forms.Select(attrs={'class': 'form-control'}),
            'image_profile': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }  
    def save(self, commit=True):
        doctor = super().save(commit=False)
        if commit:
            doctor.save()
            self.save_m2m()  
        return doctor
    
class Branch_officeForm(forms.ModelForm):
    class Meta:
        model = Branch_office
        fields = ['name','phone','address']
        widgets = {
            'branch_office': forms.Select(attrs={'class': 'form-control'}),
        }  
           
    def save(self, commit=True):
        branch_office = super().save(commit=False)
        if commit:
            branch_office.save()
        return branch_office

class DoctorAvailabilityForm(forms.ModelForm):
    WEEKDAYS_CHOICES = [
        (0, 'Seleccionar día'),
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]
    
    date = forms.DateField(label='Fecha', required=False,widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}))
    weekday = forms.ChoiceField(choices=WEEKDAYS_CHOICES, label='Día de la semana', required=False)
    start_date = forms.DateField(label='Día de inicio', required=False, widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.today().strftime('%Y-%m-%d') }))


    limit_date = forms.DateField(
        label='hasta fecha',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Slot
        fields = ['doctor', 'date','weekday',  'start_date', 'limit_date','start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        selected_date = cleaned_data.get('date')

        if selected_date and selected_date < date.today():
            self.add_error('date', 'La fecha debe ser igual o posterior a la fecha actual.')

        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', 'El end_time debe ser posterior al start_time.')
        
       
        weekday = int(cleaned_data.get('weekday'))
        start_date = cleaned_data.get('start_date')

        if not selected_date and weekday == 0 and not start_date:
            self.add_error('weekday', 'Debes seleccionar un día de la semana o una fecha.')

        return cleaned_data

    
class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['doctor', 'date', 'start_time', 'end_time', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'status': forms.Select(choices=Slot.STATUS_CHOICES),
        }

class AppointmentCreateForm(forms.ModelForm):
    slot_id = forms.IntegerField(widget=forms.HiddenInput())
   
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'start_time', 'end_time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
             'start_time': forms.TimeInput(attrs={'type': 'time', 'format': '%H:%M'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'format': '%H:%M'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(
            slot__status='available'
        ).distinct()
        self.fields['doctor'].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        notes = cleaned_data.get('notes')

          # Check if the doctor is available for the selected date and time
        if doctor and date and start_time and end_time:
              # Check if the start time is earlier than the end time
            if start_time >= end_time:
                self.add_error('start_time', 'Start time must be earlier than end time.')

            # Check if the doctor is available at the selected date and time
            slot = Slot.objects.filter(
                doctor=doctor,
                date=date,
                start_time__lte=start_time,
                end_time__gte=end_time
            ).first()

            if not slot:
                self.add_error('doctor', 'Doctor is not available at the selected date and time.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.patient = self.request.user.patient
        instance.doctor_id = self.cleaned_data['doctor'].id
    
    # Convertir las cadenas de tiempo en objetos de tiempo
        start_time = self.cleaned_data['start_time'].strftime('%H:%M')
        end_time = self.cleaned_data['end_time'].strftime('%H:%M')
        instance.start_time = start_time
        instance.end_time = end_time
    
        if commit:
            instance.save()
    
        return instance 

class AppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'start_time', 'end_time', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       

