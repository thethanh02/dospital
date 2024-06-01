from rest_framework import serializers
from authentication.models import Account
from authentication.serializers import UserSerializer

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        fields = ['id', 'username', 'user', 'role']