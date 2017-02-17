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
    Field('Registra','reference bombero',notnull = True),
    Field('Borrador','boolean',default = True,notnull = True),
    Field('Aprueba','reference bombero'),
    Field('fechaCreacion','datetime'),
    Field('fechaFinalizacion','datetime'),
    Field('fechaLlegada','datetime'),
    Field('descripcion', type='string'),
    Field('localizacion', type='string'),
    Field('tipo'))

def insertarBombero(username,password,cedula,PN,SN,PA,SA,FN,LN,G,I,emP,emA,EC,carnet,tipoS,inic):
    DB.usuario.insert(username = username,password = password)
    DB.persona.insert(cedula = cedula, 
        primer_nombre = PN,
        segundo_nombre = SN,
        primer_apellido = PA,
        segundo_apellido = SA,
        fecha_nacimiento = FN,
        lugar_nacimiento = LN,
        genero = G,
        imagen = I,
        email_principal = emP,
        email_alternativo = emA,
        estado_civil = EC)
    id_usuario = DB().select(DB.usuario.id)
    id_persona = DB().select(DB.persona.id)
    DB.bombero.insert(
        carnet = carnet,
        imagen_perfil = I,
        iniciales = inic,
        tipo_sangre = tipoS,
        id_persona = id_persona[0],
        id_usuario = id_usuario[0])

def insertarServicio(fechaCreacion,fechaFinalizacion,fechaLlegada,descripcion,localizacion,tipo):
    DB.servicio.insert(
        Registra = 1,
        Aprueba = 1,
        fechaCreacion = fechaCreacion,
        fechaFinalizacion = fechaFinalizacion,
        fechaLlegada = fechaLlegada,
        descripcion = descripcion,
        localizacion = localizacion,
        tipo = tipo)

def testCase():
    insertarBombero('gsalazar',1234,24655445,'Gerson','A.','Salazar','P.','1971/01/01','Cumana','Masculino','Gerson.jpg','blah@bleh.com','blah@blah.com','Casado',1310147,'O RH-','GS')

    insertarServicio('2017/01/03 12:35','2017/01/03 12:35','2017/01/03 16:45','Incendio edificio QYP.','USB, QYP.','IDE')
    insertarServicio('2017/01/11 15:20','2017/01/11 15:20','2017/01/11 17:55','Derrame de sustancias tóxicas en entrada de laboratorio de QYP.','USB, QYP, piso 2, lab 2A','MP')
    insertarServicio('2017/02/25 09:35','2017/02/25 09:35','2017/02/25 12:30','Incendio de vegetación en los alrededores del Pino Solitario.','Montaña USB, Pino Solitario.','IDV')
    insertarServicio('2017/01/21 11:10','2017/01/21 11:10','2017/01/22 14:55','Estudiante sufrió caida en escalera de auditorios.','USB, auditorios.','AME1')
    insertarServicio('2017/02/10 12:30','2017/02/10 12:30','2017/02/10 15:40','Rescate de búho perdido en salón de clases.','USB, ENE, piso 1, aula 110','RES2')
    insertarServicio('2017/02/21 18:15','2017/02/21 18:15','2017/02/22 19:45','Ocurrió incendio en árbol adyacente a lagunna de los patos.','USB, laguna de los patos.','IDV')
    insertarServicio('2017/01/17 14:35','2017/01/17 14:35','2017/01/17 20:45','Liberación de gases tóxicos en entrada del edificio de QYP.','USB, QYP, Entrada sur.','MP')
    insertarServicio('2017/01/21 12:20','2017/01/21 12:20','2017/01/22 16:50','Incendio de la vegetación cercana al tanque de agua de la USB.','USB, tanque de agua','Incendio Forestal')