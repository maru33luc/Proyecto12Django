from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import time
import datetime
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField('email', unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=8, verbose_name='DNI', null=True, blank=True)
    phone = models.IntegerField(default=0, null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name='Dirección', null=True, blank=True)
    city = models.CharField(max_length=40, verbose_name='Ciudad', null=True, blank=True)
    social_work = models.CharField(max_length=20, verbose_name='Obra Social', null=True, blank=True)
    sw_number = models.CharField(max_length=20, verbose_name='Número de Obra Social', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank= True, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    
    def has_appointment_with_doctor(self, doctor_id):
        return self.appointments.filter(doctor_id=doctor_id).exists()
    
    def has_appointment_with_specialist(self, specialist):
        doctors = Doctor.objects.filter(specialist=specialist)
        appointments = self.appointments.filter(doctor__in=doctors)
        return appointments.exists()
    
    def __str__(self):
        
        return self.user.get_full_name()
    
class Specialist(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
#ManytoMany

class Branch_office(models.Model):
    name = models.CharField(max_length=255, verbose_name='Branch_office', unique=True)    
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name

class Doctor(models.Model):
    # name= models.CharField(max_length=50, verbose_name='Nombre y Apellido', null=True, blank=True)
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=8, verbose_name='DNI', null=True, blank=True)
    phone = models.IntegerField(default=0, null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name='Dirección', null=True, blank=True)
    city = models.CharField(max_length=40, verbose_name='Ciudad', null=True, blank=True)
    mr_number = models.CharField(max_length=20, verbose_name='Número de Matrícula', null=True, blank=True)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank= True, on_delete=models.CASCADE)
    image_profile = models.ImageField(upload_to='doctor_images/', null=True, blank=True)
    #ManytoMany
    branch_offices = models.ManyToManyField(Branch_office, related_name='doctors')
       
    def __str__(self):
        return self.user.get_full_name()
    
# SLOTS #
class DoctorAvailability(models.Model):
   
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        abstract = True


class Slot(DoctorAvailability):   
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    #con unique_together estos campos son unicos, no puede haber dos slots iguales
    class Meta:
        unique_together = ['doctor', 'date', 'start_time', 'end_time']

    def __str__(self):
        return f"{self.doctor} - {self.date} - {self.start_time} to {self.end_time}"
    
    # TURNOS #

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('stand_by', 'Stand_by'),
        ('registered', 'Registered'),
        ('waiting', 'Waiting'),
        ('inside', 'Inside'),
        ('finished', 'Finished'),
        ('missed', 'Missed')
    ]
    STATUS_ORIGIN = [
        ('web', 'Web'),
        ('phone','Phone'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,  related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(default=datetime.time(9, 0)) # Add default start time
    end_time = models.TimeField(null=True)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='stand_by') 
    origin = models.CharField(max_length=10, choices=STATUS_ORIGIN, default='web' )
    
    def has_appointment_with_other_doctor(self):
        conflicting_appointments = Appointment.objects.exclude(id=self.id).filter(
            date=self.date,
         start_time=self.start_time
        )
        if conflicting_appointments.exists():
            conflicting_appointment = conflicting_appointments.first()
            doctor_name = conflicting_appointment.doctor.__str__()  # Obtener la representación del doctor
            formatted_date = self.date.strftime('%d %b %Y')  # Formatear la fecha como "día mes año"
            return f"Usted ya tiene un turno con el Dr. {doctor_name} el día {formatted_date} a las {self.start_time}."
                        
        return None

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.date} - {self.start_time} "
