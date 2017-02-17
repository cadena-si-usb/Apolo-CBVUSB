DB = DAL("postgres://cbvusb:1234@localhost/cbvusb")

DB.define_table('usuario', 
        Field('username', type='string', length=24, required=True, notnull=True, unique=True),
        Field('password', type='password', length=24, required=True, notnull=True))

DB.define_table('persona',
        Field('cedula', type='integer', required=True, notnull=True, unique=True),
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
        
DB.define_table('bombero', 
        Field('carnet', type='integer', required=True, notnull=True, unique=True),
        Field('imagen_perfil', type='text'),
        Field('iniciales', type='string'),
        Field('tipo_sangre', type='string'),
        Field('id_persona', type='reference persona', required=True, notnull=True, unique=True), 
        Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True))

DB.define_table('servicio',
    Field('CodServicio',unique = True,notnull = True),
    Field('Registra','reference bombero',notnull = True),
    Field('Borrador','boolean',default = True,notnull = True),
    Field('Aprueba','reference bombero'),
    Field('fechaCreacion','date'),
    Field('tipo'))

def insertBombero():
	DB.usuario.insert(username = 'gerson',password = 'mamalo')
	DB.persona.insert(cedula = 12345678, 
		primer_nombre = 'Gerson',
		segundo_nombre = 'Mamalo',
		primer_apellido = 'MamaloNo',
		segundo_apellido = 'MamaloMasFuerte',
		fecha_nacimiento = '1986/05/02',
		lugar_nacimiento = 'Mierdapolis',
		genero ='Trans',
		imagen = 'imagen',
		email_principal = 'jajajaja',
		email_alternativo = 'jejejeje',
		estado_civil = 'Gerson de Apolo')
	id_usuario = DB().select(DB.usuario.id)
	id_persona = DB().select(DB.persona.id)
	DB.bombero.insert(
		carnet = 1310147,
		imagen_perfil = 'Gay',
		iniciales = 'GG',
		tipo_sangre = 'O-',
		id_persona = id_persona[0],
		id_usuario = id_usuario[0])

insertBombero()