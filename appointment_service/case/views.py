from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from appointment.models import Appointment
from .models import Case
from .serializers import CaseSerializer
from .filters import CaseFilter

class ListCreateCaseAPIView(ListCreateAPIView):
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CaseFilter

    def get_queryset(self):
        user = self.request.user

        all_data = self.request.GET.get('all_data', 'false')

        if user.role == 'PAT':
            queryset = Case.objects.filter(patient=user.pk)
        elif user.role == 'REC':
            if all_data.lower() == 'true':
                queryset = Case.objects.all()
            else:
                queryset = Case.objects.filter(receptionist=user.pk)
        elif user.role == 'DOC':
            queryset = Case.objects.filter(appointment_case__doctor=user.pk)
            # queryset = Case.objects.all()
        else:
            queryset = Case.objects.all()

        return queryset

class RetrieveUpdateDestroyCaseAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CaseSerializer
    queryset = Case.objects.all()
    permission_classes = [IsAuthenticated]
