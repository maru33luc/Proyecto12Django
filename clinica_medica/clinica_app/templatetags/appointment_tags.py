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


@register.filter
def get_range(start, end):
    return range(start, end + 1)


@register.filter
def range_filter(value):
    return range(value)

@register.filter
def get_slot(slot_list, day, hour):
    for slot in slot_list:
        if slot.date.weekday() == day.weekday() and slot.start_time.strftime("%H:%M") == hour:
            return slot
    return None