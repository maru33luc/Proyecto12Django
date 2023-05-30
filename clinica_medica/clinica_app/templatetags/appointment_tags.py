from django import template
from clinica_app.models import Doctor

register = template.Library()

@register.filter
def has_appointment_with_doctor(patient, doctor_selected):
    # Convert the doctor_selected string to a Doctor object
    doctor = Doctor.objects.get(id=int(doctor_selected))
    # Implement the logic to check if the patient has an appointment with the selected doctor
    # For example:
    has_appointment = patient.has_appointment_with_doctor(doctor)
    return has_appointment

@register.filter
def has_appointment_with_specialist(patient, specialist):
    return patient.has_appointment_with_specialist(specialist)

# @register.filter
# def has_appointment_with_doctor(patient, doctor, date):
#     return patient.has_appointment_with_doctor(doctor, date)