# Generated by Django 4.2 on 2024-11-10 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_usuario', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('nom_usuario', models.CharField(max_length=30, unique=True)),
                ('clave', models.CharField(max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpcionForm',
            fields=[
                ('id_opcion', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('des_opcion', models.CharField(max_length=30)),
                ('num_form', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AccesoUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_opcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.opcionform')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('id_opcion', 'id_usuario')},
            },
        ),
    ]