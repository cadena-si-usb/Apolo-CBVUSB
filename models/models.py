# -*- coding: utf-8 -*-

from gluon.tools import Auth, Service, PluginManager
from gluon.contrib.login_methods.ldap_auth import ldap_auth
from datetime import *

import os

db = DAL("postgres://cbvusb:1234@localhost/cbvusb")

auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

auth.settings.login_methods.append(ldap_auth(
	server='localhost',
	base_dn='ou=Users,dc=login,dc=com'))

auth.settings.table_user_name = 'usuario'
auth.settings.extra_fields['usuario']= [Field('disable', type='boolean', default=False),
										Field('confirmed', type='boolean', default=False)]
auth.define_tables(username=True, signature=False, migrate="db.usuario")

auth.settings.create_user_groups = None
auth.settings.actions_disabled.append('register')
#auth.settings.actions_disabled.append('request_reset_password')

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:465'
mail.settings.sender = 'apolo.cbvusb@gmail.com'
mail.settings.login = 'apolo.cbvusb:0800responsable'
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# auth.enable_record_versioning(db)
db.define_table('persona',
	Field('cedula', type='integer', unique=True),
	Field('nacionalidad', type='string', required=True, notnull=True, default='V'),
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

db.define_table('telefono',
	Field('id_persona', type='reference persona', required=True, notnull=True),
	Field('codigo_telefono', type='integer', length=4, notnull=True),
	Field('numero_telefono', type='integer', length=7, notnull=True),
	migrate="db.telefono")

db.define_table('direccion',
	Field('id_persona', type='reference persona', required=True, notnull=True),
	Field('direccion_descripcion', type='string', notnull=True),
	Field('direccion_tipo', type='string', notnull=True),
	Field('direccion_ciudad', type='string', notnull=True),
	migrate="db.direccion")
		
db.define_table('bombero', 
	Field('carnet', type='integer', required=True, default=0),
	Field('imagen_perfil', type='text'),
	Field('iniciales', type='string'),
	Field('tipo_sangre', type='string'),
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('cargo', type='string', notnull=True, default='Estudiante'),
	Field('hijos', type='integer', default=0),
	Field('rango', type='string', default='Aspirante'),
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
db.auth_group.requires = IS_NOT_IN_DB(db, db.auth_group.role, error_message='Ya existe ese grupo')

db.usuario.username.requires = [IS_MATCH('^\w{6,16}$', error_message='Debe contener únicamente los caracteres: a-z, A-Z, 0-9 y _. Además debe tener una longitud de entre 6 y 16 caracteres.'),
								IS_NOT_IN_DB(db, db.usuario.username, error_message='Ya existe un usuario con ese nombre.')]

db.usuario.password.requires = [IS_MATCH('^[\w~!@#$%^&*\-+=`|(){}[\]<>\.\?\/]{4,24}$', error_message='Debe contener cualquiera de los siguientes caracteres: a-z A-Z 0-9 _!@#$%^&*\-+=`|(){}[]<>.?/ Además debe tener una longitud entre 4 y 24 caracteres.'),
								CRYPT()]

db.persona.cedula.requires = [	IS_INT_IN_RANGE(minimum=1,maximum=100000000, error_message='Número de cedula no valido.'), 
								IS_NOT_IN_DB(db,db.persona.cedula, error_message='La cédula ingresada ya existe en el sistema.')]
db.persona.nacionalidad.requires = IS_IN_SET(['V'], error_message='No es una opción válida')
db.persona.primer_nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$', error_message='Debe ser no vacío y contener sólo letras, guiones o espacios.')
db.persona.segundo_nombre.requires = IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$', error_message='Debe contener sólo letras, guiones o espacios.'))
db.persona.primer_apellido.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$', error_message='Debe ser no vacío y contener sólo letras, guiones o espacios.')
db.persona.segundo_apellido.requires = IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$', error_message='Debe contener sólo letras, guiones o espacios.'))
db.persona.fecha_nacimiento.requires = IS_EMPTY_OR([IS_DATE(format=T('%d/%m/%Y'), error_message='Debe tener el siguiente formato: dd/mm/yyyy'),
										IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date.today()-timedelta(36500), maximum=date.today()-timedelta(6000), 
													 error_message='Debe tener una edad entre 17 y 100 años')])
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
												  	'Dependencias Federales',
												  	'Extranjero'], error_message='No es una opción válida.'))
db.persona.genero.requires = IS_IN_SET(['Masculino','Femenino'], error_message='No es una opción válida.')
db.persona.imagen.requires = IS_EMPTY_OR(IS_IMAGE(extensions=('jpeg', 'png', 'jpg', 'bmp'), error_message='Debe ser un formato válido: png, jpg, jpeg o bmp.')) #IS_EMPTY_OR(IS_MATCH('^.*\.(jpg|png|jpeg|bmp)$', error_message='Debe ser un formato válido: png, jpg, jpeg o bmp'))
db.persona.email_principal.requires = IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com') # Restricción de que sea el institucional
db.persona.email_alternativo.requires = IS_EMPTY_OR(IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'))
db.persona.estado_civil.requires = IS_EMPTY_OR(IS_IN_SET(['Soltero','Casado','Divorciado','Viudo'], error_message='No es una opción válida.'))

db.telefono.codigo_telefono.requires = IS_IN_SET(['0412','0414','0416','0424','0426','0212'], error_message='Debe tener un código de área válido')
db.telefono.numero_telefono.requires = IS_INT_IN_RANGE(1000000,10000000, error_message='No es un número de teléfono válido')

db.bombero.carnet.requires = [IS_INT_IN_RANGE(1, error_message='Debe ser positivo'), IS_NOT_IN_DB(db,db.bombero.carnet, error_message='El carnet ya existe en el sistema.')]
db.bombero.iniciales.requires = IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑ]{2,4}$', error_message='Debe estar entre 2 y 4 caracteres.'))
db.bombero.tipo_sangre.requires = IS_EMPTY_OR(IS_IN_SET(['A+','A-','B+','B-','AB+','AB-','O+','O-'], error_message='Debe ser alguno de los tipos válidos.'))
db.bombero.id_persona.requires = IS_IN_DB(db,db.persona.id,'%(id)s')
db.bombero.id_usuario.requires = IS_IN_DB(db,db.persona.id,'%(id)s')
db.bombero.cargo.requires = IS_IN_SET([	'Comandante en Jefe', 
										'Primer comandante', 
										'Segundo comandante', 
										'Inspector',
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
										'Miembro de Comandancia',
										'Estudiante'], error_message='Debe seleccionar una opción.')
db.bombero.rango.requires = IS_IN_SET([	'Aspirante',
										'Alumno',
										'Bombero',
										'Distinguido',
										'Cabo Segundo',
										'Cabo Primero',
										'Sargento Segundo',
									  	'Sargento Primero',
									  	'Sargento Mayor',
									  	'Teniente',
									  	'Primer Teniente',
									  	'Capitán'
									  	'Mayor',
									  	'Teniente Coronel',
									  	'Coronel',
									  	'General',
									  	'Primer General'],
									  error_message='Debe seleccionar una opción.')
db.bombero.hijos.requires = IS_INT_IN_RANGE(0, error_message='Debe ser número positivo.')

db.direccion.direccion_tipo.requires = IS_IN_SET(['Casa','Trabajo','Otro'], error_message='Debe seleccionar una opción')
db.direccion.direccion_ciudad.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s-]+$', error_message='Debe contener sólo letras o guiones.')

db.servicio.fechaCreacion.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe tener el siguiente formato: dd/mm/yyyy')
db.servicio.fechaFinalizacion.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe tener el siguiente formato: dd/mm/yyyy')
db.servicio.fechaLlegada.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe tener el siguiente formato: dd/mm/yyyy')

db.condicion.tipo.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener sólo letras')
db.condicion.descripcion.requires = IS_IN_SET(['Activo', 'Reserva', 'Tesista','Egresado',
											   'Excomandante','Comandante', 'Alumno'], error_message='Debe seleccionar una opción.')

db.rango.tipo.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener sólo carácteres.')
db.rango.nombre.requires = IS_IN_SET(['Aspirante','Alumno','Bombero','Distinguido','Cabo Segundo','Cabo Primero','Sargento Segundo',
									  'Sargento Primero','Sargento Ayudante','Subteniente','Teniente','Capitán','Mayor'],
									  error_message='Debe seleccionar una opción.')
db.rango.abreviatura.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo letras, sin espacios.')

db.asciende.fecha.requires = [IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'),
									IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date(1998,5,15), maximum=date.today(), 
													 error_message='Introduzca una fecha entre 15/5/1998 y hoy.')]

db.condecoracion.nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener sólo carácteres.')

#db.condecoracion.descripcion.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s-,.]$', error_message='Debe contener sólo carácteres')
#No creo que esta deba ir

db.otorgada.fecha.requires = [IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'),
									IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date(1998,5,15), maximum=date.today(), 
													 error_message='Introduzca una fecha entre 15/5/1998 y hoy.')]

db.curso.nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', error_message='Debe contener sólo letras.')
db.curso.horas.requires = IS_INT_IN_RANGE(0, error_message='Debe ser un número positivo.')
db.curso.tipo.requires = IS_IN_SET(['Asistencia a taller, foro, congreso, seminario, charla, coloquio, jornada en la que haya participado como oyente',
									'Asistencia a curso de carácter teórico o alguna actividad anterior en la que haya participado en mesas de trabajo',
									'Asistencia a curso de carácter teórico y práctico','Aprobación de curso de carácter teórico',
									'Aprobación de curso de carácter teórico y práctico','Ponente de taller, foro, congreso, seminario, charla, coloquio, jornada',
									'Monitor en curso de carácter teórico o práctico',
									'Diseñador de Cursos de carácter teórico que hayan sido evaluados satisfactoriamente por personal capacitado',
									'Presentación de un Trabajo de Investigación que haya sido evaluado satisfactoriamente por personal capacitado'],
									error_message='Debe seleccionar una opción.')

db.estudio.nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo letras.')
db.estudio.nivel.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo letras.')

db.completo.fechaInicio.requires = [IS_DATE(format=T('%d/%m/%Y'), error_message='Debe tener del siguiente formato: dd/mm/yyyy'),
									IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date(1993,5,12), maximum=date.today(), 
													 error_message='Introduzca una fecha entre 12/5/1993 y hoy.')]
db.completo.fechaFin.requires = [IS_DATE(format=T('%d/%m/%Y'), error_message='Debe tener el siguiente formato: dd/mm/yyyy'),
								 IS_DATE_IN_RANGE(format=T('%d/%m/%Y'), minimum=date(1998,5,15), maximum=date.today(), 
												  error_message='Introduzca una fecha entre 12/5/1993 y hoy.')]

# INSERCIÓN DEL Administrador
if not db(db.usuario.username == 'admin').select():
	id_usuario = db.usuario.insert(username='admin', password=CRYPT()('admin')[0], first_name='Apolo', last_name='Bomberos', email='apolo.cbvusb@gmail.com', confirmed=True)
	id_persona = db.persona.insert(cedula=-1, primer_nombre='Apolo', primer_apellido='Bomberos', email_principal='apolo.cbvusb@gmail.com', genero='Masculino')
	db.bombero.insert( carnet=-1, cargo='Administrador', id_persona=id_persona, id_usuario=id_usuario)

	estudiante 	= 	auth.add_group(role='Estudiante', description='description')
	bombero 	=	auth.add_group(role='Bombero', description='description')
	gerencia   	=	auth.add_group(role='Gerencia', description='description')
	inspectoria	=	auth.add_group(role='Inspectoria', description='description')
	comandancia	=	auth.add_group(role='Comandancia', description='description')
	admin	  	=	auth.add_group(role='Administrador', description='description')

	auth.add_permission(estudiante, 'Estudiante')

	auth.add_permission(bombero, 'Estudiante')
	auth.add_permission(bombero, 'Bombero')

	auth.add_permission(gerencia, 'Estudiante')
	auth.add_permission(gerencia, 'Bombero')
	auth.add_permission(gerencia, 'Gerencia')

	auth.add_permission(inspectoria, 'Estudiante')
	auth.add_permission(inspectoria, 'Bombero')
	auth.add_permission(inspectoria, 'Gerencia')
	auth.add_permission(inspectoria, 'Inspectoria')

	auth.add_permission(comandancia, 'Estudiante')
	auth.add_permission(comandancia, 'Bombero')
	auth.add_permission(comandancia, 'Gerencia')
	auth.add_permission(comandancia, 'Inspectoria')
	auth.add_permission(comandancia, 'Comandancia')

	auth.add_permission(admin, 'Estudiante')
	auth.add_permission(admin, 'Bombero')
	auth.add_permission(admin, 'Gerencia')
	auth.add_permission(admin, 'Inspectoria')
	auth.add_permission(admin, 'Comandancia')
	auth.add_permission(admin, 'Administrador')
	
	auth.settings.everybody_group_id = estudiante

	auth.add_membership(admin, id_usuario)