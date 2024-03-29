# Generated by Django 4.1 on 2022-11-22 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0024_alter_indicadores_porcentaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicadores',
            name='cantidad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='indicadores',
            name='porcentaje',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
    ]
