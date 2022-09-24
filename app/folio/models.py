import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
	class Meta:
		default_permissions = []
		permissions = [
			('create_users', 'Crear usuarios'),
            ('view_users', 'Ver usuarios'),
			('edit_users', 'Editar usuarios'),
			('delete_users', 'Eliminar usuarios'),
			('list_users', 'Listar usuarios')
        ]
	dni = models.CharField('Número de empleado', max_length=10, unique=True)
	rfc = models.CharField('RFC corto', max_length=10, unique=True)
	username = models.CharField(
    	'username',
		blank=True,
		null=True,
        max_length=150,
        unique=True
    )
	date_joined = models.DateTimeField('date joined', default=timezone.now, blank=True)

	def save(self, *args, **kwargs):
		self.username = self.dni
		super().save(*args, **kwargs)


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
	class Meta:
		default_permissions = []
		permissions = [
			('create_requests', 'Crear solicitudes'),
            ('view_requests', 'Ver solicitudes'),
			('edit_requests', 'Editar solicitudes'),
			('delete_requests', 'Eliminar solicitudes'),
			('list_requests', 'Listar solicitudes'),
			('option', 'Opciones'),
        ]
		ordering = ['-folio']
		
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	folio = models.CharField('Folio', max_length=15, editable=False, default='No definido')
	fecha_reg = models.DateTimeField(auto_now_add=True, null=True)
	fecha_mod = models.DateTimeField(auto_now=True, null=True)
	nombre = models.CharField('Dirigido a', max_length=150)
	dependencia = models.CharField('Dependencia', max_length=150)
	motivo = models.CharField('Motivo', max_length=150)
	firmado = models.CharField('firmado', max_length=150, choices=[('autógrafo','Autógrafo'),('sifen','Sifen')])
	estatus = models.CharField('estatus', max_length=150, blank=True, default='pendiente', choices=[('pendiente','Pendiente'),('despachado','Despachado'),('cancelado','Cancelado')])
	usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, editable=False, related_name='solicitudes')

class Reducciones(models.Model):
	class Meta:
		default_permissions = []
		permissions = [
			('create_requests', 'Crear solicitudes'),
            ('view_requests', 'Ver solicitudes'),
			('edit_requests', 'Editar solicitudes'),
			('delete_requests', 'Eliminar solicitudes'),
			('list_requests', 'Listar solicitudes'),
			('option_red', 'Opciones'),
        ]
		ordering = ['-fecha_reg']

	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	folio = models.CharField(max_length=50, editable=False, default='No definido')
	fecha_reg = models.DateTimeField(auto_now_add=True, null=True)
	fecha_mod = models.DateTimeField(auto_now=True, null=True)
	folio_recepcion = models.CharField('Folio de recepción', max_length=15)
	fecha_recepcion = models.DateField('Fecha de recepción')
	rfc = models.CharField('R.F.C.', max_length=15)
	nombre_cont = models.CharField('Nombre del contribuyente', max_length=100)
	oficio = models.CharField('Determinante', max_length=100)
	ejecutivo = models.ForeignKey(Usuario, editable=False, on_delete=models.SET_NULL, null=True, related_name='reducciones')
	tipo = models.CharField('Tipo', max_length=30, choices=[('t1', 'RED. ART. 74 CFF'), ('t2', 'RED. ART. 41Y74 CFF')], null=True)
	no_oficio = models.CharField('Selecciona el no. de oficio', max_length=100, choices=(('n1', '400-58-00-02-01-2022'), ('n2', '400-58-00-02-02-2022'), ('n3', '400-58-00-03-00-2022')), null=True)
	txt_folio = models.CharField('Número de folio', max_length=100, null=True)