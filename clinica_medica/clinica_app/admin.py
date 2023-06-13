from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Doctor, Specialist, Slot, Appointment, Branch_office

# Register your models here.
#admin.site.register(User, UserAdmin)
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Specialist)
admin.site.register(Slot)
admin.site.register(Appointment)
admin.site.register(Branch_office)

