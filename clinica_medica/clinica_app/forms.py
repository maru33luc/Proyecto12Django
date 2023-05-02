from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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



class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'Please enter a correct email and password. Note that both fields may be case-sensitive.'

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError('Invalid email or password.')

            if not user.check_password(password):
                raise forms.ValidationError('Invalid email or password.')

        return self.cleaned_data
    
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')

'''
class UserSignUpCreationForm(UserCreationForm):
    class Meta:
        model = Userfields = ('username', 'email', 'first_name')

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')
'''
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
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
            model = Patient
            fields = ['dni', 'phone', 'address', 'city', 'social_work', 'sw_number', 'date_of_birth' ]
                      
    
    
class SpecialistForm(forms.ModelForm):
    
    class Meta:
        model = Specialist
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        '''
    def save(self, commit=True):
        name = self.cleaned_data['name']
        specialist = Specialist(name=name)
        if commit:
            specialist.save()
        return specialist
     '''   
    #description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    #photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    #price = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'min': 0, 'step': 0.01}))



'''

class SpecialistForm(forms.Form):
    name = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['name'].initial = instance.name

    def save(self, commit=True):
        instance = Specialist()
        if self.cleaned_data['name']:
            instance.name = self.cleaned_data['name']
        if commit:
            instance.save()
        return instance

    def update(self, instance, commit=True):
        instance.name = self.cleaned_data['name']
        if commit:
            instance.save()
        return instance
'''

class DoctorForm(forms.Form): #create Doctor
    specialist = forms.ModelChoiceField(queryset=Specialist.objects.all())
    class Meta:   #voy a especificar q modelo pertenece
        model = Doctor
        fields = ['__all__'] #campos a utilizar en este form
        widgets = {
            #'title': forms.TextInput(attrs= { 'class': 'form-control', 'placeholder': 'Write a title'}),
            #'description': forms.Textarea(attrs= { 'class': 'form-control', 'placeholder': 'Write a description'}),
            #'important': forms.CheckboxInput(attrs= { 'class': 'form-check-input m-auto'}),
            }
        
