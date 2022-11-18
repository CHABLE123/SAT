# Generated by Django 4.1 on 2022-11-18 05:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0020_alter_reducciones_options_reducciones_no_oficio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=500, verbose_name='Nombre de indicador')),
                ('mes', models.CharField(choices=[('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')], max_length=20, verbose_name='Mes')),
                ('anio', models.CharField(choices=[('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025')], max_length=5, verbose_name='Año')),
                ('fecha_reg', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['fecha_reg'],
                'permissions': [('create_ind', 'Crear indicadores'), ('view_ind', 'Ver indicadores'), ('edit_ind', 'Editar indicadores'), ('delete_ind', 'Eliminar indicadores'), ('list_ind', 'Listar indicadores'), ('option_ind', 'Opciones')],
                'default_permissions': [],
            },
        ),
        migrations.AlterModelOptions(
            name='reducciones',
            options={'default_permissions': [], 'ordering': ['fecha_reg'], 'permissions': [('create_requests', 'Crear solicitudes'), ('view_requests', 'Ver solicitudes'), ('edit_requests', 'Editar solicitudes'), ('delete_requests', 'Eliminar solicitudes'), ('list_requests', 'Listar solicitudes'), ('option_red', 'Opciones')]},
        ),
        migrations.AlterModelOptions(
            name='solicitud',
            options={'default_permissions': [], 'ordering': ['-fecha_reg'], 'permissions': [('create_requests', 'Crear solicitudes'), ('view_requests', 'Ver solicitudes'), ('edit_requests', 'Editar solicitudes'), ('delete_requests', 'Eliminar solicitudes'), ('list_requests', 'Listar solicitudes'), ('option', 'Opciones')]},
        ),
    ]
