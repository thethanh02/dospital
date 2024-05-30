from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, first_name='', last_name='', noHouse='', street='', district='', city='', country='', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)

        fullname = Fullname.objects.create(first_name=first_name, last_name=last_name)
        address = Address.objects.create(noHouse=noHouse, street=street, district=district, city=city, country=country)

        user = User.objects.create(email=email, fullname=fullname, address=address)

        account = self.model(username=username, user=user, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)

        return account

    def create_superuser(self, email, username, password=None, first_name='', last_name='', noHouse='', street='', district='', city='', country='', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, first_name, last_name, noHouse, street, district, city, country, **extra_fields)


class Fullname(models.Model):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    noHouse = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.noHouse}, {self.street}, {self.district}, {self.city}, {self.country}"


class User(models.Model):
    email = models.EmailField(unique=True)
    fullname = models.OneToOneField(Fullname, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email


class Account(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username