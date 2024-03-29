# Generated by Django 4.1 on 2022-09-15 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0016_auto_20220102_2054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solicitud',
            options={'default_permissions': [], 'ordering': ['-folio'], 'permissions': [('create_requests', 'Crear solicitudes'), ('view_requests', 'Ver solicitudes'), ('edit_requests', 'Editar solicitudes'), ('delete_requests', 'Eliminar solicitudes'), ('list_requests', 'Listar solicitudes'), ('option', 'Opciones')]},
        ),
        migrations.CreateModel(
            name='Reducciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('folio', models.CharField(default='No definido', editable=False, max_length=15)),
                ('fecha_reg', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True, null=True)),
                ('folio_recepcion', models.CharField(max_length=15, verbose_name='Folio de recepción')),
                ('fecha_recepcion', models.DateField(verbose_name='Fecha de recepción')),
                ('rfc', models.CharField(max_length=15, verbose_name='R.F.C.')),
                ('nombre_cont', models.CharField(max_length=100, verbose_name='Nombre del contribuyente')),
                ('oficio', models.CharField(max_length=100, verbose_name='Oficio')),
                ('ejecutivo', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
