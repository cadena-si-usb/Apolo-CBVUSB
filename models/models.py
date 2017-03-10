# -*- coding: utf-8 -*-

#from gluon.tools import Auth, Service, PluginManager
#from gluon.contrib.login_methods.ldap_auth import ldap_auth
from datetime import *

import os

db = DAL("postgres://cbvusb:1234@localhost/cbvusb")

auth = Auth(db, host_names=myconf.get('host.names'))
auth.settings.table_user_name = 'usuario'
auth.settings.extra_fields['usuario']= [ Field('disable', type='boolean', default=False) ]
auth.define_tables(username=True, signature=False, migrate="db.usuario")
service = Service()
plugins = PluginManager()

#auth.settings.login_methods.append(ldap_auth(
#	server='localhost',
#	base_dn='ou=Users,dc=login,dc=com',
#	manage_user=True,
#	user_firstname_attrib='cn:1',
#	user_lastname_attrib='cn:2',
#	user_mail_attrib='mail',
#	manage_groups=True,
#	db=db,
#	group_dn='ou=Groups,dc=domain,dc=com',
#	group_name_attrib='cn',
#	group_member_attrib='memberUid',
#	group_filterstr='objectClass=*'))

auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled.append('request_reset_password')

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# auth.enable_record_versioning(db)

db.define_table('persona',
	Field('cedula', type='integer', unique=True),
	Field('nacionalidad', type='string', required=True, notnull=True),
	Field('primer_nombre', type='string', required=True, notnull=True),
	Field('segundo_nombre', type='string', default=""),
	Field('primer_apellido', type='string', required=True, notnull=True),
	Field('segundo_apellido', type='string', default=""),
	Field('fecha_nacimiento', type='date'),
	Field('lugar_nacimiento', type='string'),
	Field('genero', type='string', notnull=True),
	Field('imagen', type='upload', uploadfolder=os.path.join(request.folder,'static/profile-images'),default='index.png'),
	Field('email_principal', type='string', notnull=True),
	Field('email_alternativo', type='string'),
	Field('estado_civil', type='string'),
	migrate="db.persona")

db.define_table('numero',
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('codigo_telefono', type='integer', length=4, notnull=True),
	Field('numero_telefono', type='integer', length=7, notnull=True),
	migrate="db.numero")

db.define_table('direccion',
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('direccion_descripcion', type='string', notnull=True),
	Field('direccion_tipo', type='string', notnull=True),
	Field('direccion_ciudad', type='string', notnull=True),
	migrate="db.direccion")
		
db.define_table('bombero', 
	Field('carnet', type='integer', required=True, notnull=True, unique=True),
	Field('imagen_perfil', type='text'),
	Field('iniciales', type='string'),
	Field('tipo_sangre', type='string'),
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True), 
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('cargo', type='string', notnull=True, default='Administrador'),
	Field('hijos', type='integer', default=0),
	Field('rango', type='string', default=0),
	migrate="db.bombero")

db.define_table('servicio',
	Field('Registra','reference bombero',notnull = True),
	Field('Borrador','boolean',default = True,notnull = True),
	Field('Aprueba','reference bombero'),
	Field('fechaCreacion','datetime'),
	Field('fechaFinalizacion','datetime'),
	Field('fechaLlegada','datetime'),
	Field('descripcion', type='string'),
	Field('localizacion', type='string'),
	Field('tipo'),
	migrate="db.servicio")

db.define_table('anade_imagen',
    Field('bombero', type='reference bombero'),
    Field('servicio', type='reference servicio'),
    Field('imagen', type='blob'),
    migrate="db.anade_imagen")

db.define_table('anade_observacion',
    Field('bombero', type='reference bombero'),
    Field('servicio', type='reference servicio'),
    Field('observacion', type='text'),
    migrate="db.anade_observacion")


db.define_table('comision',
    Field('servicio', type='reference servicio'),
    Field('lider', type='reference bombero'),
    migrate="db.comision")

db.define_table('comision_apoyo',
    Field('numeroacompanantes', type='integer'),
    Field('cuerpoodepartamento', type='string', length=40),
    Field('unidad', type='string', length=30),
    Field('placaunidad', type='string', length=30),
    Field('lider', type='reference persona'),
    Field('servicio', type='reference servicio'),
    migrate="db.comision_apoyo")

db.define_table('es_acompanante',
    Field('bombero', type='reference bombero'),
    Field('comision', type='reference comision'),
    migrate="db.es_acompanante")

db.define_table('es_afectado',
    Field('servicio', type='reference servicio'),
    Field('persona', type='reference persona'),
    Field('notastratamiento', type='text'),
    Field('tipo', ),
    migrate="db.es_afectado")

db.define_table('unidad',
    Field('nombre', type='string', length=30),
    Field('activa', type='boolean'),
    migrate="db.unidad")

db.define_table('unidad_utilizada_por',
    Field('unidad', type='reference unidad'),
    Field('conductor', type='reference bombero'),
    Field('comision', type='reference comision'),
    migrate="db.unidad_utilizada_por")

db.define_table('condicion',
	Field('tipo', type='string', required=True, notnull=True),
	Field('descripcion', type='string', notnull=True),
	migrate="db.condicion")

db.define_table('rango',
	Field('nombre', type='string', required=True, notnull=True),
	Field('tipo', type='string', notnull=True),
	Field('abreviatura', type='string', notnull=True),
	migrate="db.rango")

db.define_table('asciende',
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('rango', type='reference rango', required=True, notnull=True),
	Field('fecha', type='date', notnull=True),
	Field('documento', type='string', notnull=True),
	migrate="db.asciende")

db.define_table('condecoracion',
	Field('nombre', type='string', required=True, notnull=True),
	Field('descripcion', type='string', notnull=True),
	migrate="db.condecoracion")

db.define_table('otorgada',
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('condecoracion', type='reference condecoracion', required=True, notnull=True),
	Field('fecha', type='date', notnull=True),
	Field('documento', type='string', notnull=True),
	migrate="db.otorgada")

db.define_table('curso',
	Field('nombre', type='string', required=True, notnull=True),
	Field('horas', type='integer', notnull=True),
	Field('tipo', type='string', notnull=True),
	Field('escuela', type='string', notnull=True),
	migrate="db.curso")

db.define_table('estudio',
	Field('nombre', type='string', required=True, notnull=True),
	Field('nivel', type='string', notnull=True),
	Field('escuela', type='string', notnull=True),
	migrate="db.estudio")

db.define_table('completo',
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('estudio', type='reference estudio', required=True, notnull=True),
	Field('fechaInicio', type='date', notnull=True),
	Field('fechaFin', type='date', notnull=True),
	migrate="db.completo")

db.define_table('asiste',
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('curso', type='reference estudio', required=True, notnull=True),
	Field('fecha', type='date', notnull=True),
	Field('imagen', type='string', notnull=True),
	migrate="db.asiste")


# REQUIRES de la DB
db.usuario.username.requires = [IS_MATCH('^\w{6,16}$', error_message='El nombre de usuario debe:'+
																	'\n\t- Contener unicamente los caracteres: a-z, A-Z, 0-9 y _'+
																	'\n\t- Debe tener una longitud de entre 6 y 16 caracteres.'),
								IS_NOT_IN_DB(db, db.usuario.username, error_message='Ya existe un usuario con ese nombre.')]

db.usuario.password.requires = [IS_MATCH('^[\w~!@#$%^&*\-+=`|(){}[\]<>\.\?\/]{4,24}$', error_message='La contraseña debe: \n'+
																										'\n\t- Contener cualquiera de los siguientes caracteres: a-z A-Z 0-9 _!@#$%^&*\-+=`|(){}[]<>.?/'+
																										'\n\t- Debe tener una longitud entre 4 y 24 caracteres.'),
								CRYPT()]

db.persona.cedula.requires = [	IS_INT_IN_RANGE(minimum=1,maximum=100000000, error_message='Numero de cedula no valido'), 
								IS_NOT_IN_DB(db,'persona.cedula', error_message='Ya la cédula existe en el sistema')]

db.persona.nacionalidad.requires = IS_IN_SET(['V','E'], error_message='No es una opción válida')
db.persona.primer_nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s-]+$', error_message='Debe ser no vacío y contener solo letras, guiones o espacios')
db.persona.segundo_nombre.requires = IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s-]+$', error_message='Debe ser no vacío y contener solo letras, guiones o espacios'))
db.persona.primer_apellido.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s-]+$', error_message='Debe ser no vacío y contener solo letras, guiones o espacios')
db.persona.segundo_apellido.requires = IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s-]+$', error_message='Debe ser no vacío y contener solo letras, guiones o espacios'))
db.persona.fecha_nacimiento.requires = IS_EMPTY_OR([IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'),
										IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date.today()-timedelta(36500), maximum=date.today()-timedelta(6600), 
													 error_message='Debe tener una edad entre 18 y 100 años')])
db.persona.lugar_nacimiento.requires = IS_EMPTY_OR(IS_IN_SET([	'Amazonas',
													'Anzoátegui',
													'Apure',
													'Aragua',
													'Barinas',
													'Bolívar',
													'Carabobo',
													'Cojedes',
													'Delta Amacuro',
													'Distrito Capital',
													'Falcón',
													'Guárico',
													'Lara',
													'Mérida',
													'Miranda',
													'Monagas',
													'Nueva Esparta',
													'Portuguesa',
												  	'Sucre',
												  	'Táchira',
												  	'Trujillo',
												  	'Vargas',
												  	'Yaracuy',
												  	'Zulia',
												  	'Dependencias Federales'], error_message='No es una opción válida'))
db.persona.genero.requires = IS_IN_SET(['Masculino','Femenino'], error_message='No es una opción válida')
#db.persona.imagen.filename.requires = IS_EMPTY_OR(IS_MATCH('^.*\.(jpg|png|jpeg|bmp)$', error_message='Debe ser un formato válido: png, jpg, jpeg o bmp'))
db.persona.email_principal.requires = IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com') # Restricción de que sea el institucional
db.persona.email_alternativo.requires = IS_EMPTY_OR(IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'))
db.persona.estado_civil.requires = IS_EMPTY_OR(IS_IN_SET(['Soltero','Casado','Divorciado','Viudo'], error_message='No es una opción válida'))

db.bombero.carnet.requires = [IS_INT_IN_RANGE(1, error_message='Debe ser positivo'), IS_NOT_IN_DB(db,db.bombero.carnet, error_message='Ya existe el carnet en el sistema')]
db.bombero.iniciales.requires = IS_EMPTY_OR(IS_LENGTH(minsize=2,maxsize=4))
db.bombero.tipo_sangre.requires = IS_EMPTY_OR(IS_IN_SET(['A+','A-','B+','B-','AB+','AB-','O+','O-'], error_message='Debe ser alguno de los tipos válidos'))
db.bombero.id_persona.requires = IS_IN_DB(db,db.persona.id,'%(id)s')
db.bombero.id_usuario.requires = IS_IN_DB(db,db.persona.id,'%(id)s')
db.bombero.cargo.requires = IS_IN_SET([	'Administrador', 
										'Comandante en Jefe', 
										'Primer comandante', 
										'Segundo comandante', 
										'Inspector en Jefe',
										'Gerente de Riesgo', 
										'Gerente de Administración', 
										'Gerente de Educación', 
										'Gerente de Operaciones',
										'Gerente de Talento humano',
										'Sub-gerente de Riesgo', 
										'Sub-gerente de Administración', 
										'Sub-gerente de Educación', 
										'Sub-gerente de Operaciones',
										'Sub-gerente de Talento humano',
										'Miembro de Riesgo', 
										'Miembro de Administración', 
										'Miembro de Educación', 
										'Miembro de Operaciones',
										'Miembro de Talento humano',
										'Estudiante'], error_message='Debe seleccionar una opción')
db.bombero.rango.requires = IS_IN_SET([	'Aspirante',
										'Alumno',
										'Bombero',
										'Distinguido',
										'Cabo Segundo',
										'Cabo Primero',
										'Sargento Segundo',
									  	'Sargento Primero',
									  	'Sargento Ayudante',
									  	'Subteniente',
									  	'Teniente',
									  	'Capitán',
									  	'Mayor'],
									  error_message='Debe seleccionar una opción')
db.bombero.hijos.requires = IS_INT_IN_RANGE(0, error_message='Debe ser positivo')

db.direccion.direccion_tipo.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener solo letras')
db.direccion.direccion_ciudad.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s-]+$', error_message='Debe contener solo letras o guiones')

db.servicio.fechaCreacion.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.servicio.fechaFinalizacion.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.servicio.fechaLlegada.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')

db.condicion.tipo.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener solo letras')


db.condicion.descripcion.requires = IS_IN_SET(['Activo', 'Reserva', 'Tesista','Egresado',
											   'Excomandante','Comandante', 'Alumno'], error_message='Debe seleccionar una opción')
db.rango.tipo.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener sólo carácteres')

db.rango.nombre.requires = IS_IN_SET(['Aspirante','Alumno','Bombero','Distinguido','Cabo Segundo','Cabo Primero','Sargento Segundo',
									  'Sargento Primero','Sargento Ayudante','Subteniente','Teniente','Capitán','Mayor'],
									  error_message='Debe seleccionar una opción')

db.rango.abreviatura.requires = IS_MATCH('^\w+$', error_message='Debe contener solo letras sin espacios')

db.asciende.fecha.requires = [IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'),
									IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date(1998,5,15), maximum=date.today(), 
													 error_message='Introduzca una fecha entre 15/5/1998 y hoy.')]

db.condecoracion.nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener sólo carácteres')

#db.condecoracion.descripcion.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s-,.]$', error_message='Debe contener sólo carácteres')
#No creo que esta deba ir

db.otorgada.fecha.requires = [IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'),
									IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date(1998,5,15), maximum=date.today(), 
													 error_message='Introduzca una fecha entre 15/5/1998 y hoy.')]

db.curso.nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener solo letras')
db.curso.horas.requires = IS_INT_IN_RANGE(0, error_message='Debe ser positivo')
db.curso.tipo.requires = IS_IN_SET(['Asistencia a taller, foro, congreso, seminario, charla, coloquio, jornada en la que haya participado como oyente',
									'Asistencia a curso de carácter teórico o alguna actividad anterior en la que haya participado en mesas de trabajo',
									'Asistencia a curso de carácter teórico y práctico','Aprobación de curso de carácter teórico',
									'Aprobación de curso de carácter teórico y práctico','Ponente de taller, foro, congreso, seminario, charla, coloquio, jornada',
									'Monitor en curso de carácter teórico o práctico',
									'Diseñador de Cursos de carácter teórico que hayan sido evaluados satisfactoriamente por personal capacitado',
									'Presentación de un Trabajo de Investigación que haya sido evaluado satisfactoriamente por personal capacitado'],
									error_message='Debe seleccionar una opción')


db.estudio.nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener solo letras')
db.estudio.nivel.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener solo letras')

db.completo.fechaInicio.requires = [IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'),
									IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date(1993,5,12), maximum=date.today(), 
													 error_message='Introduzca una fecha entre 12/5/1993 y hoy.')]

db.completo.fechaFin.requires = [IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'),
								 IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date(1998,5,15), maximum=date.today(), 
												  error_message='Introduzca una fecha entre 12/5/1993 y hoy.')]
