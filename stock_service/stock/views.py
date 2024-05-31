from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Item, Stock
from .serializers import ItemSerializer, StockSerializer

class ListCreateItemAPIView(ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]

class RetrieveUpdateDestroyItemAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]

class ListCreateStockAPIView(ListCreateAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    permission_classes = [IsAuthenticated]

class RetrieveUpdateDestroyStockAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    permission_classes = [IsAuthenticated]
