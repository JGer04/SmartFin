# Generated by Django 4.2 on 2024-11-02 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentaBalance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentabalance',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
