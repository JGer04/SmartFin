# Generated by Django 4.2 on 2024-11-16 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_alter_usuario_id_usuario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesousuario',
            options={},
        ),
        migrations.AlterModelOptions(
            name='opcionform',
            options={},
        ),
        migrations.RenameField(
            model_name='opcionform',
            old_name='des_opcion',
            new_name='descripcion',
        ),
        migrations.AlterUniqueTogether(
            name='accesousuario',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='opcionform',
            name='num_form',
        ),
        migrations.AddField(
            model_name='opcionform',
            name='tipo_usuario',
            field=models.CharField(choices=[('ADM', 'Administrador'), ('AFE', 'Analista Financiero del Área de Energía'), ('AFM', 'Analista Financiero del Área de Minería')], default='ADM', max_length=3),
        ),
        migrations.AlterField(
            model_name='accesousuario',
            name='id_opcion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accesos', to='usuario.opcionform'),
        ),
        migrations.AlterField(
            model_name='accesousuario',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accesos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='opcionform',
            name='id_opcion',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='accesousuario',
            unique_together={('id_usuario', 'id_opcion')},
        ),
        migrations.AlterModelTable(
            name='accesousuario',
            table='acceso_usuario',
        ),
        migrations.AlterModelTable(
            name='opcionform',
            table=None,
        ),
    ]