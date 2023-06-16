from django.urls import path, include
from django.contrib import admin
admin.autodiscover()
from . import views
from django.contrib.auth import views as auth_views
from .views import SpecialistsListView

urlpatterns = [
    path('', views.index, name="index"),
    path('services/', views.services, name="services"),
    path('staff', views.staff, name="staff"),
    path('appointment', views.appointment, name="appointment"),
    path('contact', views.contact, name="contact"),
    path('about_us', views.about_us, name="about_us"),
    path('welcome', views.welcome, name='welcome'),
    path('log_in', views.login_view, name='log_in'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),  
    path('logout', views.logout_view, name='logout'),  
    ### doctors ###
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    #### patients ####
    path('patient/create/', views.patient_create, name='patient_create'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:pk>/update/', views.patient_update, name='patient_update'),

    ### appointments###
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/detail/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/show/', views.appointment_show, name='appointment_show'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('patient_appointments/', views.patient_appointments, name='patient_appointments'),
    path('appointments/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    ##doctor poner en admin##
  
    path('contacto', views.contacto, name="contacto"), 
    # path('doctor_availability/<int:doctor_id>/', views.doctor_availability_detail, name='doctor_availability_detail')
    ## slots ##
    path('slots/', views.slot_view, name='slot_view'),
    path('edit_slot/<int:pk>/', views.edit_slot, name='edit_slot'),
    path('delete_slot/<int:pk>/', views.delete_slot, name='delete_slot'),
    
    #### ADMIN ####
    
    #brnach_office
    path('admin/branch_offices', views.branch_offices, name="branch_offices"), 
    path('admin/branch_office/<int:pk>/', views.branch_office_detail, name='branch_office_detail'),
    path('admin/branch_office/new/', views.branch_office_create, name='branch_office_create'),
    path('admin/branch_office/<int:pk>/update/', views.branch_office_update, name='branch_office_update'),
    path('admin/branch_office/<int:pk>/delete/', views.branch_office_delete, name='branch_office_delete'),
    #appointments
    path('admin/appointments/doctors_consults', views.doctors_consults, name='doctors_consults'), 
    path('admin/appointments/patients_consults', views.patients_consults, name='patients_consults'), 

    path('admin/home_admin', views.home_admin, name='home_admin'),
    path('admin/login_admin', views.login_admin, name='login_admin'),
    #patients#
    
    path('patients', views.patients, name="patients"), 
    path('admin/patient/create/', views.patient_create_admin, name='patient_create_admin'),
    path('admin/patient/<int:pk>/update/', views.patient_update_admin, name='patient_update_admin'),
    path('admin/patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    #specialist#
    path('admin/specialist_list', views.SpecialistsListView.as_view(), name='specialist_list'),
    # path('admin/specialist_list', views.specialist_list, name='specialist_list'),
    path('admin/specialist/<int:pk>/', views.specialist_detail, name='specialist_detail'),
    path('admin/specialist/new/', views.specialist_create, name='specialist_create'),
    path('admin/specialist/<int:pk>/update/', views.specialist_update, name='specialist_update'),
    path('admin/specialist/<int:pk>/delete/', views.specialist_delete, name='specialist_delete'),
    
    #doctors#

    path('admin/doctors', views.doctors, name="doctors"), 
    
    path('admin/doctor/new/', views.doctor_create, name='doctor_create'),
    path('admin/doctor/<int:pk>/update/', views.doctor_update, name='doctor_update'),
    path('admin/doctor/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    
]




