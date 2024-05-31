import django_filters
from .models import Appointment

class AppointmentFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter()
    receptionist = django_filters.NumberFilter()
    doctor = django_filters.NumberFilter()

    class Meta:
        model = Appointment
        fields = ['patient', 'receptionist', 'doctor']
