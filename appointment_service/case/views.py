from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Case
from .serializers import CaseSerializer
from .filters import CaseFilter

class ListCreateCaseAPIView(ListCreateAPIView):
    serializer_class = CaseSerializer
    queryset = Case.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = CaseFilter

class RetrieveUpdateDestroyCaseAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CaseSerializer
    queryset = Case.objects.all()
    permission_classes = [IsAuthenticated]
