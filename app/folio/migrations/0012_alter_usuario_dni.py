# Generated by Django 3.2.9 on 2021-12-27 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0011_alter_solicitud_firmado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.CharField(max_length=10, unique=True, verbose_name='Número de empleado'),
        ),
    ]
