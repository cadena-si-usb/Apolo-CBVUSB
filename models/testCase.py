def insertarBombero(username,password,cedula,PN,SN,PA,SA,FN,LN,G,I,emP,emA,EC,carnet,tipoS,inic,nacionalidad="V"):
    db.usuario.insert(username = username,password = password)
    db.persona.insert(cedula = cedula,
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
        estado_civil = EC,
        nacionalidad = nacionalidad)
    id_usuario = db().select(db.usuario.id)
    id_persona = db().select(db.persona.id)
    db.bombero.insert(
        carnet = carnet,
        imagen_perfil = I,
        iniciales = inic,
        tipo_sangre = tipoS,
        id_persona = 1,#id_persona[len(id_persona)-1],
        id_usuario = 1)#id_usuario[len(id_persona)-1])

def insertarServicio(horaCreacion, fechaCreacion, horaFinalizacion, fechaFinalizacion, descripcion, localizacion, tipo, borrador=True, aprueba=None, aprobado=False):
    db.servicio.insert(
        Registra = 1,
        Aprueba = aprueba,
        aprobado = aprobado,
        Borrador = borrador,
        horaCreacion = horaCreacion,
        fechaCreacion = fechaCreacion,
        horaFinalizacion = horaFinalizacion,
        fechaFinalizacion = fechaFinalizacion,
        descripcion = descripcion,
        localizacion = localizacion,
        tipo = tipo)

def testCase():
    #insertarBombero('gsalazar',1234,24444444,'Gerson','A.','Salazar','P.','1971/01/01','Cumana','Masculino','Gerson.jpg','blah@bleh.com','blah@blah.com','Casado',1311347,'O RH-','GS')

    insertarServicio('12:35','2017/01/03','16:45','2017/01/03','Incendio edificio QYP.','USB, QYP.','IDE',True, True, aprobado = True)
    insertarServicio('15:20','2017/01/11','17:55','2017/01/11','Derrame de sustancias tóxicas en entrada de laboratorio de QYP.','USB, QYP, piso 2, lab 2A','MP',False, True)
    insertarServicio('09:35','2017/02/25','12:30','2017/02/25','Incendio de vegetación en los alrededores del Pino Solitario.','Montaña USB, Pino Solitario.','IDV',True, True, aprobado = True)
    insertarServicio('11:10','2017/01/21','14:55','2017/01/22','Estudiante sufrió caida en escalera de auditorios.','USB, auditorios.','AME1',False)
    insertarServicio('12:30','2017/02/10','15:40','2017/02/10','Rescate de búho perdido en salón de clases.','USB, ENE, piso 1, aula 110','RES2',False, aprobado = True)
    insertarServicio('18:15','2017/02/21','19:45','2017/02/22','Ocurrió incendio en árbol adyacente a lagunna de los patos.','USB, laguna de los patos.','IDV',True)
    insertarServicio('14:35','2017/01/17','20:45','2017/01/17','Liberación de gases tóxicos en entrada del edificio de QYP.','USB, QYP, Entrada sur.','MP',True, aprobado = True)


    #db.unidad.insert(id=1,nombre='-Ninguna-')
    #db.unidad.insert(id=2,nombre='A1')
    #db.unidad.insert(id=3,nombre='A2')
    #db.unidad.insert(id=4,nombre='L1')
    #db.unidad.insert(id=5,nombre='L2')
    #db.unidad.insert(id=6,nombre='M1')
    #db.unidad.insert(id=7,nombre='M2')

#testCase()
