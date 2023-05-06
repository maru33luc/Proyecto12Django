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
    path('patients', views.patients, name="patients"), 
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:pk>/update/', views.patient_update, name='patient_update'),
    path('patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('admin/doctors', views.doctors, name="doctors"), 
    path('contacto', views.contacto, name="contacto"), 
    
    
    #### ADMIN ####
    #specialist#
    path('admin/specialist_list', views.specialist_list, name='specialist_list'),
    path('admin/<int:pk>/', views.specialist_detail, name='specialist_detail'),
    path('admin/new/', views.specialist_create, name='specialist_create'),
    path('admin/<int:pk>/update/', views.specialist_update, name='specialist_update'),
    path('admin/<int:pk>/delete/', views.specialist_delete, name='specialist_delete'),
    #doctors#


    
]





