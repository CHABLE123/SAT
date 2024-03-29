# Generated by Django 4.1 on 2022-09-20 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0018_reducciones_tipo_alter_reducciones_ejecutivo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reducciones',
            options={'default_permissions': [], 'ordering': ['-fecha_reg']},
        ),
        migrations.AlterField(
            model_name='reducciones',
            name='folio',
            field=models.CharField(default='No definido', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='reducciones',
            name='tipo',
            field=models.CharField(choices=[('t1', 'Tipo 1'), ('t2', 'Tipo 2')], default='t1', max_length=30, null=True, verbose_name='Tipo'),
        ),
    ]
