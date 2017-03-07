#from gluon.tools import Auth, Service, PluginManager
#from gluon.contrib.login_methods.ldap_auth import ldap_auth

db = DAL("postgres://cbvusb:1234@localhost/cbvusb")

auth = Auth(db, host_names=myconf.get('host.names'))
auth.settings.table_user_name = 'usuario'
auth.define_tables(username=True, signature=False)
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

#auth.settings.actions_disabled.append('register')

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
"""
db.define_table('usuario', 
	Field('username', type='string', length=512, unique=True),
	Field('password', type='password', readable=False, length=512)
	migrate="db.usuario")
"""

db.define_table('persona',
	Field('cedula', type='string', unique=True),
	Field('primer_nombre', type='string', required=True, notnull=True),
	Field('segundo_nombre', type='string'),
	Field('primer_apellido', type='string', required=True, notnull=True),
	Field('segundo_apellido', type='string'),
	Field('fecha_nacimiento', type='date', notnull=True),
	Field('lugar_nacimiento', type='string', notnull=True),
	Field('genero', type='string', notnull=True),
	Field('imagen', type='text'),
	Field('email_principal', type='string', notnull=True),
	Field('email_alternativo', type='string'),
	Field('estado_civil', type='string', notnull=True),
	migrate="db.persona")

db.define_table('numero',
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('codigo_telefono', type='integer', length=4, notnull=True),
	Field('numero_telefono', type='integer', length=7, notnull=True),
	migrate="db.numero")

db.define_table('direccion',
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('direccion_descripcion', type='string', notnull=True),
	Field('direccion_tipo', type='string', notnull=True),
	Field('direccion_ciudad', type='string', notnull=True),
	migrate="db.direccion")
		
db.define_table('bombero', 
	Field('carnet', type='integer', required=True, notnull=True, unique=True),
	Field('imagen_perfil', type='text'),
	Field('iniciales', type='string'),
	Field('tipo_sangre', type='string', required=True),
	Field('id_persona', type='reference persona', required=True, notnull=True, unique=True), 
	Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
	Field('cargo', type='string', notnull=True, default='Administrador'),
	Field('hijos', type='integer', default=0),
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
	migrate="db.curso")

db.define_table('estudio',
	Field('nombre', type='string', required=True, notnull=True),
	Field('nivel', type='string', notnull=True),
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

db.define_table('escuela',
	Field('nombre', type='string', required=True, notnull=True),
	migrate="db.escuela")

db.define_table('dicta',
	Field('escuela', type='reference escuela', required=True, notnull=True),
	Field('curso', type='reference curso', required=True, notnull=True),
	migrate="db.dicta")

db.define_table('ofrece',
	Field('escuela', type='reference escuela', required=True, notnull=True),
	Field('estudio', type='reference estudio', required=True, notnull=True),
	migrate="db.ofrece")

# REQUIRES de la DB
db.usuario.username.requires = [IS_MATCH('^\w{6,16}', error_message='El nombre de usuario debe:'+
																	'\n\t- Contener unicamente los caracteres: a-z, A-Z, 0-9 y _'+
																	'\n\t- Debe tener una longitud de entre 6 y 16 caracteres.'),
								IS_NOT_IN_DB(db, db.usuario.username, error_message='Ya existe un usuario con ese nombre.')]

db.usuario.password.requires = [IS_MATCH('^[\w~!@#$%^&*\-+=`|(){}[\]<>\.\?\/]{8,24}$', error_message='La contraseña debe: \n'+
																										'\n\t- Contener cualquiera de los siguientes caracteres: a-z A-Z 0-9 _!@#$%^&*\-+=`|(){}[]<>.?/'+
																										'\n\t- Debe tener una longitud entre 8 y 24 caracteres.'),
								CRYPT()]

db.persona.cedula.requires = IS_MATCH('^[VE]-\d+$', error_message='Debe tener un formato válido V-XXXXXXX o E-XXXXXXXX')
db.persona.primer_nombre.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
db.persona.segundo_nombre.requires = IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres'))
db.persona.primer_apellido.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
db.persona.segundo_apellido.requires = IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres'))
db.persona.fecha_nacimiento.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.persona.lugar_nacimiento.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
db.persona.genero.requires = IS_IN_SET(['Masculino','Femenino'], error_message='No es una opción válida')
db.persona.email_principal.requires = IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com') # Restricción de que sea el institucional
db.persona.email_alternativo.requires = IS_EMPTY_OR(IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'))
db.persona.estado_civil.requires = IS_IN_SET(['Soltero','Casado','Divorciado','Viudo'], error_message='No es una opción válida')

db.bombero.carnet.requires = IS_INT_IN_RANGE(0, error_message='Debe ser positivo')
db.bombero.iniciales.requires = IS_EMPTY_OR(IS_LENGTH(minsize=2,maxsize=4))
db.bombero.tipo_sangre.requires = IS_IN_SET(['A+','A-','B+','B-','AB+','AB-','O+','O-'], error_message='Debe ser alguno de los tipos válidos')
db.bombero.id_persona.requires = IS_IN_DB(db,db.persona.id,'%(id)s')
db.bombero.id_usuario.requires = IS_IN_DB(db,db.persona.id,'%(id)s')
db.bombero.cargo.requires = IS_IN_SET(['Administrador', 'Comandante en Jefe', 'Primer comandante', 'Segundo comandante', 
									'Inspector en Jefe', 'sub-Inspector',
									'Gerente de Riesgo', 'Gerente de Administración', 'Gerente de Educación', 'Gerente de Operaciones','Gerente de Talento humano',
									'Coordinador de Riesgo', 'Coordinador de Administración', 'Coordinador de Educación', 'Coordinador de Operaciones','Coordinador de Talento humano',
									'Miembro de Riesgo', 'Miembro de Administración', 'Miembro de Educación', 'Miembro de Operaciones','Miembro de Talento humano',
									'Estudiante'])
db.bombero.hijos.requires = IS_INT_IN_RANGE(0, error_message='Debe ser positivo')

db.direccion.direccion_tipo.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.direccion.direccion_ciudad.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')

db.servicio.fechaCreacion.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.servicio.fechaFinalizacion.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.servicio.fechaLlegada.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')

db.condicion.tipo.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
#Falta IN_SET tipos de condicion
db.condicion.descripcion.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')

db.rango.tipo.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
#Falta IN_SET tipos de condicion
db.rango.nombre.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.rango.abreviatura.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')

db.asciende.fecha.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')

db.condecoracion.nombre.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
#Falta IN_SET tipos de condicion
db.condecoracion.descripcion.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')

db.otorgada.fecha.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')

db.curso.nombre.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.curso.horas.requires = IS_INT_IN_RANGE(0, error_message='Debe ser positivo')

db.estudio.nombre.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.estudio.nivel.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')

db.completo.fechaInicio.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.completo.fechaFin.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')

db.asiste.fecha.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')

db.escuela.nombre.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')