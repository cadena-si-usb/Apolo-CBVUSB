db = DAL("postgres://cbvusb:1234@localhost/cbvusb")

db.define_table('usuario', 
        Field('username', type='string', length=24, required=True, notnull=True, unique=True),
        Field('password', type='password', length=24, required=True, notnull=True),
        migrate="db.usuario")

db.define_table('persona',
        Field('cedula', type='string', unique=True),
        Field('primer_nombre', type='string', required=True, notnull=True),
        Field('segundo_nombre', type='string'),
        Field('primer_apellido', type='string', required=True, notnull=True),
        Field('segundo_apellido', type='string', notnull=True),
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
        Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
        Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
        Field('tipo', type='string', required=True, notnull=True),
        Field('descripcion', type='string', notnull=True),
        migrate="db.condicion")

db.define_table('rango',
        Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
        Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
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
        Field('id_persona', type='reference persona', required=True, notnull=True, unique=True),
        Field('id_usuario', type='reference usuario', required=True, notnull=True, unique=True),
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

# REQUIRES de la DB
db.usuario.username.requires = IS_ALPHANUMERIC(error_message='Debe contener únicamente caracteres alfanuméricos')
db.usuario.password.requires = IS_MATCH('')

db.persona.cedula.requires = IS_MATCH('^[VE]-\d+$', error_message='Debe tener un formato válido V-XXXXXXX o E-XXXXXXXX')
db.persona.primer_nombre.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.persona.segundo_nombre.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.persona.primer_apellido.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.persona.segundo_apellido.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.persona.fecha_nacimiento.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.persona.lugar_nacimiento.requires = IS_MATCH('^\w+$', error_message='Debe contener sólo carácteres')
db.persona.genero.requires = IS_IN_SET(['Masculino','Femenino'], error_message='No es una opción válida')
db.persona.email_principal.requires = IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com') # Restricción de que sea el institucional
db.persona.email_alternativo.requires = IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com')
db.persona.estado_civil.requires = IS_IN_SET(['Soltero','Casado','Divorciado','Viudo'], error_message='No es una opción válida')

db.bombero.carnet.requires = IS_INT_IN_RANGE(0, error_message='Debe ser positivo')
db.bombero.iniciales.requires = IS_LENGTH(minsize=2,maxsize=4)
db.bombero.tipo_sangre.requires = IS_IN_SET(['A+','A-','B+','B-','AB+','AB-','O+','O-'], error_message='Debe ser alguno de los tipos válidos')
db.bombero.id_persona.requires = IS_IN_DB(db,db.persona.id,'%(id)s')
db.bombero.id_usuario.requires = IS_IN_DB(db,db.persona.id,'%(id)s')
db.bombero.hijos.requires = IS_INT_IN_RANGE(0, error_message='Debe ser positivo')

db.servicio.fechaCreacion.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.servicio.fechaFinalizacion.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
db.servicio.fechaLlegada.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')

