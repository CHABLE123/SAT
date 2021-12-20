import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
	dni = models.CharField('Numero de empleado', max_length=10, unique=True)
	rfc = models.CharField('RFC corto', max_length=10, unique=True)
	rol = models.CharField('rol', max_length=150, choices=[('operativo','Operativo'),('administrador','Administrador')])
	username = models.CharField(
    	'username',
		blank=True,
		null=True,
        max_length=150,
        unique=True
    )
	date_joined = models.DateTimeField('date joined', default=timezone.now, blank=True)
	#USERNAME_FIELD = "email"
	#REQUIRED_FIELDS = []

"""
class usuario(models.Model):
	nombre = models.CharField('Nombre', max_length=150)
	apellidop = models.CharField('Apellido paterno', max_length=150)
	apellidom = models.CharField('Apellido materno', max_length=150)
	dni = models.CharField('Numero de empleado', max_length=10, unique=True)
	rfc = models.CharField('RFC corto', max_length=10, unique=True)
	rol = models.CharField('rol', max_length=150, choices=[('operativo','Operativo'),('administrador','Administrador')])
"""
class solicitud(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	folio = models.CharField('Folio', max_length=15, editable=False, default='No definido')
	fecha_reg = models.DateTimeField(auto_now=True, null=True)
	fecha_mod = models.DateTimeField(auto_now_add=True, null=True)
	nombre = models.CharField('Dirigido a', max_length=150)
	dependencia = models.CharField('Dependencia', max_length=150)
	motivo = models.CharField('Motivo', max_length=150)
	archivo = models.FileField(upload_to='archivo/%Y/%m/%d', null=True, blank=True)
	firmado = models.CharField('firmado', max_length=150, choices=[('autografo','Autografo'),('sifen','Sifen')])
	estatus = models.CharField('estatus', max_length=150, default='pendiente', choices=[('pendiente','Pendiente'),('comprobado','Comprobado'),('cancelado','Cancelado')], editable=False)
	