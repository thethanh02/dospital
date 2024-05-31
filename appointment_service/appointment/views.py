from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Appointment
from .serializers import AppointmentSerializer

class Health(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):
        return Response({"status": "If You See This Service Appointment Is Running"})


class ProtectedView(APIView):
    def get(self, request):
        return Response({"Service Appointment Received User ID": self.request.user.pk, "uid": self.request.user.uid, "role": self.request.user.role})

class ListCreateAppointmentAPIView(ListCreateAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     # Assign the user who created the appointment
    #     serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyAppointmentAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
