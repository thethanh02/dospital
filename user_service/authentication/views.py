from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, AccountSerializer, MyTokenObtainPairSerializer
from .models import Account
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer