from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User, Account, Fullname, Address
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['uid'] = user.id
        token['username'] = user.username
        token['is_admin'] = user.is_admin

        return token


class FullnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fullname
        fields = ['first_name', 'last_name']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['noHouse', 'street', 'district', 'city', 'country']


class UserSerializer(serializers.ModelSerializer):
    fullname = FullnameSerializer()
    address = AddressSerializer()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'is_active': {'read_only': True}}

    def create(self, validated_data):
        fullname_data = validated_data.pop('fullname', None)
        address_data = validated_data.pop('address', None)

        fullname = Fullname.objects.create(
            **fullname_data) if fullname_data else None
        address = Address.objects.create(
            **address_data) if address_data else None

        user = User.objects.create(
            fullname=fullname, address=address, **validated_data)
        return user

    def update(self, instance, validated_data):
        fullname_data = validated_data.pop('fullname', None)
        address_data = validated_data.pop('address', None)

        if fullname_data and instance.fullname:
            fullname_serializer = FullnameSerializer(
                instance.fullname, data=fullname_data, partial=True)
            if fullname_serializer.is_valid(raise_exception=True):
                fullname_serializer.save()

        if address_data and instance.address:
            address_serializer = AddressSerializer(
                instance.address, data=address_data, partial=True)
            if address_serializer.is_valid(raise_exception=True):
                address_serializer.save()

        return super().update(instance, validated_data)


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        fields = ['username', 'password', 'user']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()

        account = Account(user=user, **validated_data)
        account.set_password(validated_data['password'])
        account.save()
        return account

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data and instance.user:
            user_serializer = UserSerializer(
                instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user