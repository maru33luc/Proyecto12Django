from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank= True, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
   
    def __str__(self):
        
        return self.user.get_full_name()
    
class Specialist(models.Model):
    name = models.CharField(max_length=255, unique=True)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank= True, on_delete=models.CASCADE)
    image_profile = models.ImageField(upload_to='doctor_images/', null=True, blank=True)
   
    def __str__(self):
        return self.mr_number
    
        