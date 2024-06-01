from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Appointment
from .serializers import AppointmentSerializer
from .filters import AppointmentFilter
import requests
from django.utils import timezone

class Health(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):
        return Response({"status": "If You See This Service Appointment Is Running"})


class ProtectedView(APIView):
    def get(self, request):
        return Response({"Service Appointment Received User ID": self.request.user.pk, "uid": self.request.user.uid, "role": self.request.user.role})

class ListCreateAppointmentAPIView(ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = AppointmentFilter

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PAT':
            queryset = Appointment.objects.filter(patient=user.pk, appointment_time__gte=timezone.now()).order_by('appointment_time')
        elif user.role == 'REC':
            queryset = Appointment.objects.filter(appointment_time__gte=timezone.now()).order_by('appointment_time')
        elif user.role == 'DOC':
            queryset = Appointment.objects.filter(doctor=user.pk, appointment_time__gte=timezone.now()).order_by('appointment_time')
        else:
            queryset = Appointment.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        patient_ids = queryset.values_list('patient', flat=True).distinct()

        headers = {'Authorization': request.headers.get('Authorization')}
        user_service_url = 'http://0.0.0.0:8000/api/user/batch/'
        response = requests.post(user_service_url, json={'user_ids': list(patient_ids)}, headers=headers)
        
        if response.status_code == 200:
            patient_info = response.json()
        else:
            patient_info = {}
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'patient_info': patient_info})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'patient_info': patient_info})
        return Response(serializer.data)

    # def perform_create(self, serializer):
    #     # Assign the user who created the appointment
    #     serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyAppointmentAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
