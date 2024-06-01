from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Bill
from .serializers import BillSerializer
from .filters import BillFilter

class ListCreateBillAPIView(ListCreateAPIView):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = BillFilter

class RetrieveUpdateDestroyBillAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()
    permission_classes = [IsAuthenticated]
