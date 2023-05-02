from django.urls import path, include
from django.contrib import admin
admin.autodiscover()
from . import views
from django.contrib.auth import views as auth_views
#from .views import CustomLoginView, CustomLogoutView




urlpatterns = [
    path('', views.index, name="index"),
    path('services/', views.services, name="services"),
    path('staff', views.staff, name="staff"),
    path('appointment', views.appointment, name="appointment"),
    path('contact', views.contact, name="contact"),
    path('about_us', views.about_us, name="about_us"),
  
    path('signup', views.signup, name='signup'),

#aqui esta las rutas para acceso ususarios
    path('signout', views.signout, name= 'signout'),
    path('signin', views.signin, name='signin'),
    path('welcome', views.welcome, name='welcome'),

   
  
  
    path('log_in', views.login_view, name='log_in'),

    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),  
    path('logout', views.logout_view, name='logout'),  
    path('patient/create/', views.patient_create, name='patient_create'),
    path('patients', views.patients, name="patients"), 
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:pk>/update/', views.patient_update, name='patient_update'),
    path('patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    path('contacto', views.contacto, name="contacto"), 
     # path('login1/', CustomLoginView.as_view(), name='login'),
   # path('logout/', CustomLogoutView.as_view(), name='logout'),
   #### patients ####
    
    
    
    
    #### ADMIN ####
    #specialist#
    path('admin/specialist_list', views.specialist_list, name='specialist_list'),
    path('admin/<int:pk>/', views.specialist_detail, name='specialist_detail'),
    path('admin/new/', views.specialist_create, name='specialist_create'),
    path('admin/<int:pk>/update/', views.specialist_update, name='specialist_update'),
    path('admin/<int:pk>/delete/', views.specialist_delete, name='specialist_delete'),
    #doctors#



    
]

'''
    path('create_task/', views.create_task, name='create_task' ),
    path('task_detail/<int:task_id>', views.task_detail, name='task_detail' ),
    path('task_detail/<int:task_id>/complete', views.task_complete, name='task_complete' ),
    path('task_detail/<int:task_id>/delete', views.task_delete, name='task_delete' ),
'''




