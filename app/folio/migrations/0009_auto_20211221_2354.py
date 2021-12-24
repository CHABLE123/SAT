# Generated by Django 3.2.9 on 2021-12-22 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0008_alter_solicitud_estatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solicitud',
            options={'default_permissions': [], 'permissions': [('create_requests', 'Crear solicitudes'), ('view_requests', 'Ver solicitudes'), ('edit_requests', 'Editar solicitudes'), ('delete_requests', 'Eliminar solicitudes'), ('list_requests', 'Listar solicitudes')]},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'default_permissions': [], 'permissions': [('create_users', 'Crear usuarios'), ('view_users', 'Ver usuarios'), ('edit_users', 'Editar usuarios'), ('delete_users', 'Eliminar usuarios'), ('list_users', 'Listar usuarios')]},
        ),
    ]