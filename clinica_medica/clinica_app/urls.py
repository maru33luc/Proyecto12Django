from django.urls import path, include
from django.contrib import admin
admin.autodiscover()
from . import views
from django.contrib.auth import views as auth_views


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
    #### patients ####
    path('patient/create/', views.patient_create, name='patient_create'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:pk>/update/', views.patient_update, name='patient_update'),

    ### appointments###
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    # path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    ##doctor poner en admin##
    path('doctor_availability/', views.doctor_availability, name='doctor_availability'),
    path('edit_availability/<int:pk>/', views.edit_availability, name='edit_availability'),
    path('delete_availability/<int:pk>/', views.delete_availability, name='delete_availability'),
    
    path('contacto', views.contacto, name="contacto"), 
    
    
    #### ADMIN ####
    path('admin/home_admin', views.home_admin, name='home_admin'),
    path('admin/login_admin', views.login_admin, name='login_admin'),
    #patients#
    path('patients', views.patients, name="patients"), 
    path('admin/patient/create/', views.patient_create_admin, name='patient_create_admin'),
    path('admin/patient/<int:pk>/update/', views.patient_update_admin, name='patient_update_admin'),
    path('admin/patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    #specialist#
    path('admin/specialist_list', views.specialist_list, name='specialist_list'),
    path('admin/specialist/<int:pk>/', views.specialist_detail, name='specialist_detail'),
    path('admin/specialist/new/', views.specialist_create, name='specialist_create'),
    path('admin/specialist/<int:pk>/update/', views.specialist_update, name='specialist_update'),
    path('admin/specialist/<int:pk>/delete/', views.specialist_delete, name='specialist_delete'),
    
    #doctors#

    path('admin/doctors', views.doctors, name="doctors"), 
    path('admin/doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('admin/doctor/new/', views.doctor_create, name='doctor_create'),
    path('admin/doctor/<int:pk>/update/', views.doctor_update, name='doctor_update'),
    path('admin/doctor/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    
]





