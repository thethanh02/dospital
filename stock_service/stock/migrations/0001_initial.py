# Generated by Django 4.1.13 on 2024-06-01 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('cost_price', models.IntegerField()),
                ('sell_price', models.IntegerField()),
                ('manufacturer', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('purchase_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_item', to='stock.item')),
            ],
        ),
    ]
