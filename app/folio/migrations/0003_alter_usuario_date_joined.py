# Generated by Django 4.0 on 2021-12-14 06:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0002_alter_usuario_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='date joined'),
        ),
    ]