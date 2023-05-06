from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime, date, timedelta
import re
from .models import User, Patient, Doctor, Specialist
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

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
        
   
class DoctorForm(forms.Form): #create Doctor
    first_name = forms.CharField(label="Nombre: ", required=True)
    last_name = forms.CharField(label="Apellido: ", required=True)
    email = forms.EmailField(label="Email: ", required=True)
    specialist = forms.ModelChoiceField(queryset=Specialist.objects.all())
    class Meta:   #voy a especificar q modelo pertenece
        model = Doctor
        fields = ['__all__'] #campos a utilizar en este form
        widgets = {
            'specialist': forms.Select(attrs={'class': 'form-control'}),
            'image_profile': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        
            #'title': forms.TextInput(attrs= { 'class': 'form-control', 'placeholder': 'Write a title'}),
            #'description': forms.Textarea(attrs= { 'class': 'form-control', 'placeholder': 'Write a description'}),
            #'important': forms.CheckboxInput(attrs= { 'class': 'form-check-input m-auto'})
        }
