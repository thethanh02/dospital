from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient_info = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = '__all__'

    def get_patient_info(self, obj):
        return self.context.get('patient_info', {}).get(str(obj.patient), None)