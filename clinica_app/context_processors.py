from .models import Patient
def patient_id(request):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user)
            
            # patient = Patient.objects.filter(user=request.user)
            patient_id = patient.id
        except Patient.DoesNotExist:
            patient_id = None
    else:
        patient_id = None
    return {'patient_id': patient_id}
