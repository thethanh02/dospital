# Generated by Django 4.1.13 on 2024-05-30 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noHouse', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Fullname',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.address')),
                ('fullname', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.fullname')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('role', models.CharField(choices=[('REC', 'receptionist'), ('PAT', 'patient'), ('DOC', 'doctor')], default='PAT', max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='authentication.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
