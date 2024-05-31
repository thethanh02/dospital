from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Item, Bill
from .serializers import ItemSerializer, BillSerializer

class ListCreateItemAPIView(ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]

class RetrieveUpdateDestroyItemAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]

class ListCreateBillAPIView(ListCreateAPIView):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()
    permission_classes = [IsAuthenticated]

class RetrieveUpdateDestroyBillAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()
    permission_classes = [IsAuthenticated]
