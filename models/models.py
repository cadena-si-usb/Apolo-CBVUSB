db = DAL('postgres://web2py:web2py@localhost/CVBUSB') # Lo que sea que sea la base de datos

db.define_table('usuario', 
		Field('username', type='string', length=24, required=True, notnull=True, unique=True),
		Field('password', type='password', length=24, required=True, notnull=True))

db.define_table('persona',
		Field('cedula', type='integer', required=True, notnull=True, unique=True)
		Field('primer_nombre', type='string', required=True, notnull=True),
		Field('segundo_nombre', type='string'),
		Field('primer_apellido', type='string', required=True, notnull=True),
		Field('segundo_apellido', type='string', required=True, notnull=True),
		Field('fecha_nacimiento', type='date', required=True, notnull=True),
		Field('lugar_nacimiento', type='string', required=True, notnull=True),
		Field('genero', type='string', required=True, notnull=True),
		Field('imagen', type='text'),
		Field('email_principal', type='string', required=True, notnull=True),
		Field('email_alternativo', type='string'),
		Field('estado_civil', type='string', required=True, notnull=True))
		
db.define_table('bombero', 
		Field('carnet', type='integer', required=True, notnull=True, unique=True),
		Field('imagen_perfil', type='text'),
		Field('iniciales', type='string'),
		Field('tipo_sangre', type='string'),
		Field('id_persona', type='reference persona', required=True, notnull=True, unique=True), 
		Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True))