# Generated by Django 4.2 on 2024-11-10 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_alter_usuario_options_alter_usuario_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesousuario',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='opcionform',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='accesousuario',
            table='accesoUsuario',
        ),
        migrations.AlterModelTable(
            name='opcionform',
            table='optionForm',
        ),
    ]