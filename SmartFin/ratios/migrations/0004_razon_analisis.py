# Generated by Django 4.2 on 2024-11-17 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratios', '0003_alter_razon_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='razon',
            name='analisis',
            field=models.CharField(default='Sin análisis', max_length=300),
        ),
    ]