# -*- coding: utf-8 -*-
from gluon.serializers import json
from datetime import datetime
from collections import defaultdict
#import pdfkit xD
#from emailManager import emailManager Mientras no se use esta comentado xD

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman las vistas de "Mis servicios"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista para listar "Mis servicios aprobados"
@auth.requires_login()
def msapproved():

    # id de usuario logeado al sistema
    user_id = auth.user.id

    # id de bombero logeado al sistema
    bombero_id = db(db.bombero.id_usuario == user_id).select()[0].id

    services = db(db.servicio.aprobado == True).select(orderby=~db.servicio.fechaCreacion)
    misServiciosAprobados = list()

    # De entre servicios aprobados solo los que el bombero registro
    for servicio in services:
        if servicio.Registra == bombero_id:
            misServiciosAprobados.append(servicio)

    return dict(services=misServiciosAprobados)

# Vista para listar "Mis servicios pendientes por aprobación"
@auth.requires_login()
def mspending():

    # id de usuario logeado al sistema
    user_id = auth.user.id

    # id de bombero logeado al sistema
    bombero_id = db(db.bombero.id_usuario == user_id).select()[0].id

    services = db((db.servicio.Borrador == False) & (db.servicio.aprobado == False)).select(orderby=~db.servicio.fechaCreacion)
    misServiciosPendientes = list()

    # De entre servicios pendientes solo los que el bombero registro
    for servicio in services:
        if servicio.Registra == bombero_id:
            misServiciosPendientes.append(servicio)

    return dict(services=misServiciosPendientes)

# Vista para listar "Mis servicios guardados en borradores"
@auth.requires_login()
def msdraft():

    # id de usuario logeado al sistema
    user_id = auth.user.id

    # id de bombero logeado al sistema
    bombero_id = db(db.bombero.id_usuario == user_id).select()[0].id

    services = db((db.servicio.Borrador == True) & (db.servicio.aprobado == False)).select(orderby=~db.servicio.fechaCreacion)
    misServiciosBorradores = list()

    # De entre servicios borradores solo los que el bombero registro
    for servicio in services:
        if servicio.Registra == bombero_id:
            misServiciosBorradores.append(servicio)

    return dict(services=misServiciosBorradores)

# Botón para eliminar un servicio en cualquier vista de "Mis servicios"
@auth.requires_login()
def deleteMyService():
    serviceId = request.vars.row_id
    db(db.servicio.id == serviceId).delete()
    redirect(URL('services','myservices'))

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman las vistas de "Gestionar servicios"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista principal de "Gestionar Servicios"
@auth.requires_login()
def allservices():
    services = db(db.servicio.aprobado == True).select(orderby=~db.servicio.fechaCreacion)
    registran = list()
    for servicio in  services:
        bombero = db(db.bombero.id == servicio.Registra).select()[0]
        persona = db(db.persona.id == bombero.id_persona).select()[0]
        registra = nombreBombero(persona.id)
        registran.append(registra)
    return dict(services=services,registran=registran)

# Vista para listar "Mis Servicios" en los que aparezco
@auth.requires_login()
def myservices():

    # ID de cuenta de usuario del bombero
    userId = auth.user.id

    servicios = db(db.servicio.aprobado == True).select(orderby=~db.servicio.fechaCreacion)
    misServicios = list()
    registran = list()

    # Todos los servicios
    for servicio in servicios:

        # Registrador
        bombero = db(db.bombero.id == servicio.Registra).select()[0]
        persona = db(db.persona.id == bombero.id_persona).select()[0]
        registra = nombreBombero(persona.id)
        registran.append(registra)

        miServicio = False

        # Comisiones del servicio
        comisiones = db(db.comision.servicio == servicio.id).select()
        for comision in comisiones:

            # Jefe de comision
            try:
                lider = db(db.bombero.id == comision.lider).select()[0]
                if int(lider.id_usuario) == int(userId):
                    # Usuario conectado es jefe de comision
                    miServicio = True
            except:
                pass

            # Acompanantes de comision
            acompanantes = db(db.es_acompanante.comision == comision.id).select()
            for acompanante in acompanantes:
                try:
                    bombero = db(db.bombero.id == acompanante.bombero).select()[0]
                    if int(bombero.id_usuario) == int(userId):
                        # Usuario conectado es acompanante de comision
                        miServicio = True
                except:
                    pass

            # Conductor de comision
            unidades = db(db.unidad_utilizada_por.comision == comision.id).select()
            for unidad in unidades:
                try:
                    if int(unidad.conductor) == int(userId):
                        # Usuario conectado es conductor de comision
                        miServicio = True
                except:
                    pass

        # Si usuario esta en alguna comision entonces agregamos a mis servicios
        if miServicio:
            misServicios.append(servicio)

    return dict(services=misServicios,registran=registran)

# Botón para eliminar un servicio en cualquier vista de "Gestionar servicios"
@auth.requires_login()
def deleteService():
    serviceId = request.vars.row_id
    db(db.servicio.id == serviceId).delete()
    redirect(URL('services','allservices'))

# Comisiones del servicio
@auth.requires_login()
def obtenerComisiones(serviceId):
    comisionCounter = 1
    comisiones = list()
    comisionRows = db(db.comision.servicio == serviceId).select()
    for comisionRow in comisionRows:
        comision = dict()

        try:
            # Jefe de comision
            bomberoRow = db(db.bombero.id == comisionRow.lider).select()[0]
            comision['jefe'] = nombreBombero(bomberoRow.id_persona)
        except:
            continue

        # Unidad
        try:
            unidadUtilizadaRow = db(db.unidad_utilizada_por.comision == comisionRow.id).select()[0]
            if unidadUtilizadaRow.unidad is None:
                comision["unidad"] = None
                comision["conductor"] = None
            else:
                unidadRow = db(db.unidad.id == unidadUtilizadaRow.unidad).select()[0]
                comision["unidad"] = unidadRow.nombre
                bomberoRow = unidadUtilizadaRow.conductor
                comision["conductor"] = nombreBombero(bomberoRow.id_persona)
        except:
            comision["unidad"] = None
            comision["conductor"] = None

        # Acompanantes
        acompanantes = list()
        esAcompananteSet = db(db.es_acompanante.comision == comisionRow.id).select()
        for esAcompananteRow in esAcompananteSet:
            try:
                bomberoRow = esAcompananteRow.bombero
                nombre = nombreBombero(bomberoRow.id_persona)
                acompanantes.append(nombre)
            except:
                continue

        comision["acompanantes"] = acompanantes
        comision["numero"] = comisionCounter
        comisiones.append(comision)
        comisionCounter += 1

    return comisiones

# Afectados del servicio
@auth.requires_login()
def obtenerAfectados(serviceId):
    afectadoCounter = 1
    afectados = list()
    afectadoRows = db(db.es_afectado.servicio == serviceId).select()
    for afectadoRow in afectadoRows:

        afectado = dict()
        afectado["notastratamiento"] = afectadoRow.notastratamiento
        afectado["tipo"] = afectadoRow.tipo

        try:
            personaRow = db(db.persona.id == afectadoRow.persona).select()[0]
        except:
            continue

        afectado["cedula"] = personaRow.cedula
        afectado["primer_nombre"] = personaRow.primer_nombre
        afectado["segundo_nombre"] = personaRow.segundo_nombre
        afectado["primer_apellido"] = personaRow.primer_apellido
        afectado["segundo_apellido"] = personaRow.segundo_apellido
        afectado["sexo"] = personaRow.genero
        afectado["email_principal"] = personaRow.email_principal
        afectado["email_alternativo"] = personaRow.email_alternativo

        afectado["numeros"] = list()
        numeroRows = db(db.telefono.id_persona == personaRow.id).select()
        for numeroRow in numeroRows:
            afectado["numeros"].append(str(numeroRow.numero_telefono))

        afectado["counter"] = afectadoCounter
        afectados.append(afectado)
        afectadoCounter += 1

    return afectados


# Comisiones de apoyo
@auth.requires_login()
def obtenerApoyoExterno(serviceId):
    externoCounter = 1
    externos = list()
    externoRows = db(db.comision_apoyo.servicio == serviceId).select()
    for externoRow in externoRows:

        externo = dict()

        externo["cuerpoDepartamento"] = externoRow.cuerpoodepartamento
        externo["jefe"] = externoRow.lider
        externo["numAcomp"] = externoRow.numeroacompanantes
        externo["unidad"] = externoRow.unidad
        externo["placa"] = externoRow.placaunidad
        externo["comentario"] = externoRow.comentario
        externo["counter"] = externoCounter

        if externo["numAcomp"] == None: externo["numAcomp"] = ""
        if externo["unidad"] == None: externo["unidad"] = ""
        if externo["placa"] == None: externo["placa"] = ""

        externos.append(externo)
        externoCounter += 1

    return externos

# Vista para visualizar servicio
@auth.requires_login()
def displayService():
    serviceId = request.vars.id
    nombreBomberos = obtenerNombreBomberos()

    # Info basica del servicio
    service = db(db.servicio.id == serviceId).select()[0]

    # Comisiones del servicio
    comisiones = obtenerComisiones(serviceId)

    # Afectados del servicio
    afectados = obtenerAfectados(serviceId)

    # Comisiones de apoyo
    externos = obtenerApoyoExterno(serviceId)

    """url_service = URL('services','exportarServicio', args=[request.args[1],auth.user.id])
    bombero = db((db.bombero.id==request.args[1]) & (db.persona.id == db.bombero.id_persona) & (db.usuario.id==db.bombero.id_usuario)).select().first()
    db(db.constancia.id_solicitante == request.args[1]).delete()
    os.system('wkhtmltopdf '+request.env.http_host+url_service+' constancia.pdf')
    mail.send(to=[bombero.persona.email_principal],
                subject='Solicitud de constancia: Aprobada',
                message='Estimado '+bombero.usuario.username+' su solicitud de constancia ha sido aprobada por el departamente de Talento Humano.\n\n'+
                        'Adjunto se envía la constancia correspondiente:\n\n'+
                        'Sistema de Gestión Apolo. CBVUSB.',
                attachments = mail.Attachment('constancia.pdf', content_id='constancia'))
    os.system('rm constancia.pdf')"""

    return dict(service=service,comisiones=comisiones,afectados=afectados,externos=externos)

def nombreBombero(id):
    personaRow = db(db.persona.id == id).select()[0]

    # 1er nombre
    nombre = personaRow.primer_nombre

    # 2do nombre
    if personaRow.segundo_nombre is not None:
        nombre += " " + personaRow.segundo_nombre

    # 1er apellido
    nombre += " " + personaRow.primer_apellido

    # 2do nombre
    if personaRow.segundo_apellido is not None:
        nombre += " " + personaRow.segundo_apellido

    return nombre

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista principal (Servicios)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista principal de "Servicios"
@auth.requires_login()
def index():
    services = db(db.servicio.aprobado == True).select(orderby=~db.servicio.fechaCreacion)
    registran = list()
    for servicio in  services:
        bombero = db(db.bombero.id == servicio.Registra).select()[0]
        persona = db(db.persona.id == bombero.id_persona).select()[0]
        registra = nombreBombero(persona.id)
        registran.append(registra)
    return dict(services=services,registran=registran)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Buscar servicios"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista principal de "Buscar servicios"
@auth.requires_login()
def search(): return dict()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Registrar servicio"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtener nombres de bomberos para autocompletado de registro de comisiones
@auth.requires_login()
def obtenerNombreBomberos():
    bomberos = db(db.bombero.id_persona == db.persona.id).select()
    nombreBomberos = dict()
    for bombero in bomberos:
        nombre =    bombero.persona.primer_nombre    + " " +\
                    bombero.persona.primer_apellido
        clave = bombero.bombero.id
        nombreBomberos[nombre] = clave

    return nombreBomberos

# Obtener nombres de unidades para autocompletado de registro de unidades de comisiones
@auth.requires_login()
def obtenerNombreUnidades():
    unidades = db().select(db.unidad.ALL)
    nombreUnidades = dict()
    for unidad in unidades:
        nombre = unidad.nombre
        clave = unidad.id
        nombreUnidades[nombre] = clave

    return nombreUnidades

@auth.requires_login()
def registrarComisiones(request):

    idBomberos = obtenerNombreBomberos()
    idUnidades = obtenerNombreUnidades()

    for commissionCounter in range(1,int(request.vars["commissionsCount"])+1):

        # Procesar cada comision agregada
        if request.vars["commissionTitle"+str(commissionCounter)] is not None:

            # Jefe de comision
            jefeComision = request.vars["commissionBoss"+str(commissionCounter)]

            # Acompanantes
            acompanantes = list()
            for acompanantesCounter in range(1,int(request.vars["commissionMembersCount"+str(commissionCounter)])+1):
                if request.vars["commissionMember"+str(commissionCounter)+"-"+str(acompanantesCounter)] is not None:
                    acompanantes.append(request.vars["commissionMember"+str(commissionCounter)+"-"+str(acompanantesCounter)])

            # Unidades
            UnidadesCounter = 1
            unidades = list()
            conductores = list()
            while request.vars["unitValue"+str(commissionCounter)+"-"+str(UnidadesCounter)] is not None:
                unidades.append(request.vars["unitValue"+str(commissionCounter)+"-"+str(UnidadesCounter)])
                conductores.append(request.vars["commissionDriver"+str(commissionCounter)+"-"+str(UnidadesCounter)])
                UnidadesCounter+=1


            ####################################
            #### Almacenar en base de datos ####
            ####################################

            # Guardar comision
            db.comision.insert(
                servicio = request.vars["id"],
                lider = idBomberos.get(jefeComision))

            # Obtener ID de la comision
            comisionID = db.comision.id.max()
            comisionID = db().select(comisionID).first()[comisionID]

            # Guardar acompanantes
            for acompanante in acompanantes:
                db.es_acompanante.insert(
                    bombero = idBomberos.get(acompanante),
                    comision = comisionID)

            # Guardar unidades y conductores
            for unidadComision, conductorComision in zip(unidades,conductores):
                db.unidad_utilizada_por.insert(
                    unidad = idUnidades.get(unidadComision),
                    conductor = idBomberos.get(conductorComision),
                    comision = comisionID)

@auth.requires_login()
def registrarAfectados(request):

    for affectedCounter in  range(1,int(request.vars["affectedCount"])+1):

    # Procesar cada afectado agregado
        if request.vars["affectedTitle"+str(affectedCounter)] is not None:

            # Nombres del afectado
            nombre1 = request.vars["affectedFirstName"+str(affectedCounter)]
            nombre2 = request.vars["affectedSecondName"+str(affectedCounter)]

            # Apellidos del afectado
            apellido1 = request.vars["affectedFirstSurname"+str(affectedCounter)]
            apellido2 = request.vars["affectedSecondSurname"+str(affectedCounter)]

            tipoAfectado = request.vars["affectedType"+str(affectedCounter)]

            cedulaAfectado = request.vars["affectedCI"+str(affectedCounter)]

            sexo = request.vars["affectedGender"+str(affectedCounter)]

            notasYtratamiento = request.vars["affectedNotes"+str(affectedCounter)]

            emailPrincipal = request.vars["affectedEmail"+str(affectedCounter)+"-1"]
            emailAlternativo = request.vars["affectedEmail"+str(affectedCounter)+"-2"]

            # Registrar como persona si no esta registrado
            registrado = False
            for i in db(db.persona.cedula == cedulaAfectado).select():
                registrado = True
                personaID = i.id

            if not registrado:
                db.persona.insert(
                    cedula = cedulaAfectado,
                    nacionalidad = "Desconocido",
                    primer_nombre = nombre1,
                    segundo_nombre = nombre2,
                    primer_apellido = apellido1,
                    segundo_apellido = apellido2,
                    fecha_nacimiento = "01/01/0001",
                    lugar_nacimiento = "Desconocido",
                    genero = sexo,
                    email_principal = emailPrincipal,
                    email_alternativo = emailAlternativo,
                    estado_civil = "soltero")
                # Obtener ID de la persona
                personaID = db.persona.id.max()
                personaID = db().select(personaID).first()[personaID]


            # Registrar como afectado
            db.es_afectado.insert(
                servicio = request.vars["id"],
                persona = personaID,
                notastratamiento = notasYtratamiento,
                tipo = tipoAfectado)

            # Telefonos
            #telfCounter = 1
            #for telfCounter in range(1,int(request.vars["phoneCount"+str(affectedCounter)])+1):
            #    if request.vars["affectedPhone"+str(affectedCounter)+"-"+str(telfCounter)] is not None:
            #        request.vars["affectedPhone"+str(affectedCounter)+"-"+str(telfCounter)]
            #        telf = request.vars["affectedPhone"+str(affectedCounter)+"-"+str(telfCounter)]
            #        db.telefono.insert(
            #            id_persona = personaID,
            #            codigo_telefono = 0,
            #            numero_telefono = telf)


@auth.requires_login()
def registrarApoyoExterno(request):

    for comisionCounter in range(1,int(request.vars["apoyoExtCount"])+1):
        # Procesar cada afectado agregado
        if request.vars["comisionExtTitle"+str(comisionCounter)] is not None:

            cuerpoDeptExt = request.vars["cuerpoDepartamento"+str(comisionCounter)]
            numAcompanantes = request.vars["numAcomp"+str(comisionCounter)]

            unitExt = request.vars["unitExtValue"+str(comisionCounter)+"-1"]
            unitExtPlaca = request.vars["unitExtPlaca"+str(comisionCounter)+"-1"]

            jefe = request.vars["jefe"+str(comisionCounter)]
            comentarioExt = request.vars["unitExtNotes"+str(comisionCounter)]

            # Registrar como afectado
            db.comision_apoyo.insert(
                numeroacompanantes = numAcompanantes,
                cuerpoodepartamento = cuerpoDeptExt,
                unidad = unitExt,
                placaunidad = unitExtPlaca,
                lider = jefe,
                comentario = comentarioExt,
                servicio = request.vars["id"])


# Obtener jerarquia de rangos de los bomberos
@auth.requires_login()
def jerarquiaRangos():

    rangos = dict()
    rangos["Aspirante"] = 0
    rangos["Alumno"] = 1
    rangos["Bombero"] = 2
    rangos["Distinguido"] = 3
    rangos["Cabo Segundo"] = 4
    rangos["Cabo Primero"] = 5
    rangos["Sargento Segundp"] = 6
    rangos["Sargento Primero"] = 7
    rangos["Sargento Mayor"] = 8
    rangos["Teniente"] = 9
    rangos["Primer Teniente"] = 10
    rangos["Capitán y Mayor"] = 11
    rangos["Teniente Coronel"] = 12
    rangos["Coronel"] = 13
    rangos["General"] = 14
    rangos["Primer General"] = 15

    return rangos

# Funcion para calcular si bombero es de mayor rango que el aprobador actual
@auth.requires_login()
def esMayor(bombero, aprobador):

    rangos = jerarquiaRangos()

    if rangos[bombero.rango] > rangos[aprobador["rango"]]:
        return True
    elif rangos[bombero.rango] < rangos[aprobador["rango"]]:
        return False
    else:
        return bombero.carnet < aprobador["carnet"]


# Funcion para agregar bombero que debe aprobar el servicio
@auth.requires_login()
def agregarAprobador(servicioID):

    # Bombero aprobador de servicio
    aprobador = dict()
    aprobador["carnet"] = -1
    aprobador["id"] = None

    comisionRows = db(db.comision.servicio == servicioID).select()
    for comisionRow in comisionRows:
        try:
            bomberoRow = db(db.bombero.id == comisionRow.lider).select().first()

            # Bombero es seleccionado para ser aprobador de servicio
            if aprobador["carnet"] == -1 or esMayor(bomberoRow, aprobador):
                aprobador["rango"] = bomberoRow.rango
                aprobador["carnet"] = bomberoRow.carnet
                aprobador["id"] = bomberoRow.id
        except:
            continue

    servicio = db(db.servicio.id == servicioID).select().first()
    servicio.Aprueba = aprobador["id"]
    servicio.update_record()


# Vista principal de "Registrar servicio"
@auth.requires_login()
def register():

   # Form rellenado y submiteado por usuario
    if request.env.request_method == 'POST':
        # Guardar borrador de form
        if request.vars['borrador'] == "True":
            borrador = True
        # Registrar form completo
        else:
            borrador = False

        # id de bombero que registra servicio
        idBombero = db(db.bombero.id_usuario == auth.user.id).select()[0];

        # Registrar servicio en base de datos
        db.servicio.insert(
            Registra = idBombero,
            Aprueba = None,
            Borrador = borrador,
            horaCreacion = request.vars['horaCreacion'],
            fechaCreacion = request.vars['fechaCreacion'],
            horaFinalizacion = request.vars['horaFinalizacion'],
            fechaFinalizacion = request.vars['fechaFinalizacion'],
            descripcion = request.vars['descripcion'],
            localizacion = request.vars['localizacion'],
            tipo = request.vars['tipo'])

        # Obtener ID de servicio registrado
        servicioId = db.servicio.id.max()
        request.vars["id"] = db().select(servicioId).first()[servicioId]

        # Registrar datos de comisiones, afectados y apoyo externo
        registrarComisiones(request)
        registrarAfectados(request)
        registrarApoyoExterno(request)

        # Agregar bombero que debe aprobar servicio
        agregarAprobador(request.vars["id"])

        # Borrador guardado. Redireccionar a edicion de borrador para continuar con registro
        if borrador:
            # Obtener ID del servicio recien registrado
            servicioRegistradoID = db.servicio.id.max()
            servicioRegistradoID = db().select(servicioRegistradoID).first()[servicioRegistradoID]
            redirect(URL('services','editDraft.html',vars=dict(id=servicioRegistradoID)))

        # Servicio registrado. Redireccionar a pagina principal
        else:
            redirect(URL('services','index.html'))

    # Pagina de registro inicial (method get)
    else:

        # Obtener ID de ultimo servicio registrado
        # ID de nuevo servicio sera ultimo ID + 1
        ultimoServicioId = db.servicio.id.max()
        ultimoServicioId = db().select(ultimoServicioId).first()[ultimoServicioId]

        # Caso especial para 1er servicio registrado
        if ultimoServicioId is None:
            ultimoServicioId = 0

        # Obtener nombres de bomberos para autocompletado de registro de comisiones
        nombreBomberos = obtenerNombreBomberos()
        nombreUnidades = obtenerNombreUnidades()

        # Obtener array con los nombres de los bomberos (brutal pal javaScript)
        nombresArray = []
        for nombre in nombreBomberos: nombresArray.append(nombre)

        return dict(nuevoServicioId=ultimoServicioId + 1, nombreBomberos=nombreBomberos, nombreUnidades=nombreUnidades, nombresArray=nombresArray)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Editar borrador"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@auth.requires_login()
def eliminarComisiones(request):
    serviceId = request.vars['id']
    db(db.comision.servicio == serviceId).delete()

@auth.requires_login()
def eliminarAfectados(request):
    serviceId = request.vars['id']
    db(db.es_afectado.servicio == serviceId).delete()

@auth.requires_login()
def eliminarApoyoExterno(request):
    serviceId = request.vars['id']
    db(db.comision_apoyo.servicio == serviceId).delete()

@auth.requires_login()
def editDraft():

    if request.env.request_method == 'POST':

        servicio = db(db.servicio.id == request.vars['id']).select().first()
        servicio.id = request.vars['id']
        servicio.tipo = request.vars['tipo']
        servicio.horaCreacion = request.vars['horaCreacion']
        servicio.fechaCreacion = request.vars['fechaCreacion']
        servicio.horaFinalizacion = request.vars['horaFinalizacion']
        servicio.fechaFinalizacion = request.vars['fechaFinalizacion']
        servicio.descripcion = request.vars['descripcion']
        servicio.localizacion = request.vars['localizacion']

        eliminarComisiones(request)
        eliminarAfectados(request)
        eliminarApoyoExterno(request)

        registrarComisiones(request)
        registrarAfectados(request)
        registrarApoyoExterno(request)

        # Registrar form
        if request.vars['borrador'] == "False":
            servicio.Borrador = False
            servicio.update_record()
            redirect(URL('services','index.html'))
        # Guardar borrador y continuar edicion
        else:
            servicio.update_record()
            redirect(URL('services','editDraft.html',vars=dict(id=request.vars['id'])))

    else:

        serviceId = request.vars.id
        service = db(db.servicio.id == serviceId).select()[0]

        nombreBomberos = obtenerNombreBomberos()

        # Comisiones del servicio
        comisiones = obtenerComisiones(serviceId)

        # Afectados del servicio
        afectados = obtenerAfectados(serviceId)

        # Comisiones de apoyo
        externos = obtenerApoyoExterno(serviceId)

        # Obtener nombres de unidades
        nombreUnidades = obtenerNombreUnidades()

        # Obtener array con los nombres de los bomberos (brutal pal javaScript)
        nombresArray = []
        for nombre in nombreBomberos: nombresArray.append(nombre)

        return dict(service=service, nombreBomberos=nombreBomberos, comisiones=comisiones, afectados=afectados, externos=externos, nombreUnidades=nombreUnidades, nombresArray=nombresArray)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Aprobar Servicio"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def obtenerNombreMes(mes):
    if mes=="0":
        mesNombre = "Todos"
    elif mes=="1":
        mesNombre = "Enero"
    elif mes=="2":
        mesNombre = "Febrero"
    elif mes=="3":
        mesNombre = "Marzo"
    elif mes=="4":
        mesNombre = "Abril"
    elif mes=="5":
        mesNombre = "Mayo"
    elif mes=="6":
        mesNombre = "Junio"
    elif mes=="7":
        mesNombre = "Julio"
    elif mes=="8":
        mesNombre = "Agosto"
    elif mes=="9":
        mesNombre = "Septiembre"
    elif mes=="10":
        mesNombre = "Octubre"
    elif mes=="11":
        mesNombre = "Noviembre"
    elif mes=="12":
        mesNombre = "Diciembre"
    return mesNombre

def obtenerDuracionServicio(servicio):

    horaInicio = datetime.strptime(servicio.horaCreacion, '%H:%M').time()
    fechaInicio = datetime.strptime(servicio.fechaCreacion, "%d/%m/%Y")
    tiempoInicio = datetime.combine(fechaInicio, horaInicio)

    horaFin = datetime.strptime(servicio.horaFinalizacion, '%H:%M').time()
    fechaFin = datetime.strptime(servicio.fechaFinalizacion, "%d/%m/%Y")
    tiempoFin = datetime.combine(fechaFin, horaFin)

    return (tiempoFin - tiempoInicio).total_seconds() / 3600

# Mostrar servicios pendientes por mi aprobacion
@auth.requires_login()
def approve():
    services = db((db.servicio.Borrador == False) & (db.servicio.aprobado == False) & (db.servicio.Aprueba == auth.user.id)).select(orderby=~db.servicio.fechaCreacion)
    registran = list()
    for servicio in  services:
        bombero = db(db.bombero.id == servicio.Registra).select()[0]
        persona = db(db.persona.id == bombero.id_persona).select()[0]
        registra = nombreBombero(persona.id)
        registran.append(registra)

    return dict(services=services,registran=registran)

@auth.requires_login()
def approveService():

    serviceId = request.vars.id
    nombreBomberos = obtenerNombreBomberos()

    # Info basica del servicio
    service = db(db.servicio.id == serviceId).select()[0]

    # Comisiones del servicio
    comisiones = obtenerComisiones(serviceId)

    # Afectados del servicio
    afectados = obtenerAfectados(serviceId)

    # Comisiones de apoyo
    externos = obtenerApoyoExterno(serviceId)

    return dict(service=service,comisiones=comisiones,afectados=afectados,externos=externos)

# Funcion para mandar correo con notificaciones
@auth.requires_login()
def mandarCorreo(servicio,emailSubject,emailMessage,emailAttachments = None):

    bombero = db(db.bombero.id == servicio.Registra).select().first()
    persona = db(db.persona.id == bombero.id_persona).select().first()
    correo  = persona.email_principal

    mail.send(to=correo,
        subject=emailSubject,
        message=emailMessage,
        attachments = emailAttachments)


@auth.requires_login()
def validarServicio():

    # Aprobar servicio
    servicio = db(db.servicio.id == request.vars['id']).select().first()
    servicio.aprobado = True
    servicio.update_record()

    # Mandar correo de notificacion de aprobado
    mandarCorreo(servicio, "Estado servicio "+str(servicio.id)+" : Validado",
        'Su registro de servicio ' + str(servicio.id) + ' ha sido validado.\n\n'+
        'Sistema de Gestión Apolo. CBVUSB.')

    services = db((db.servicio.Borrador == False) & (db.servicio.aprobado == False) & (db.servicio.Aprueba == auth.user.id)).select(orderby=~db.servicio.fechaCreacion)
    redirect(URL('services','approve',vars=dict(services=services)))


@auth.requires_login()
def editarServicio():
    # Editar servicio pendiente por aprobacion
    redirect(URL('services','editDraft.html',vars=dict(id=request.vars['id'])))

@auth.requires_login()
def rechazarServicio():

    # Eliminar servicio
    servicio = db(db.servicio.id == request.vars['id']).select().first()
    db(db.servicio.id == request.vars["id"]).delete()

    # Mandar correo de notificacion de rechazado
    mandarCorreo(servicio, "Estado servicio "+str(servicio.id)+" : Rechazado",
        'Su registro de servicio ' + str(servicio.id) + ' ha sido rechazado.\n\n'+
        'Sistema de Gestión Apolo. CBVUSB.')

    services = db((db.servicio.Borrador == False) & (db.servicio.aprobado == False) & (db.servicio.Aprueba == auth.user.id)).select(orderby=~db.servicio.fechaCreacion)
    redirect(URL('services','approve',vars=dict(services=services)))


# Vista de "Estadisticas"
def stadistics():

    # Mes solicitado para mostrar estadisticas de servicios
    mes = request.vars['mes'];
    if mes == None:
        mes = "0"

    # Ano solicitado para mostrar estadisticas de servicios
    ano = request.vars['ano'];
    if ano == None:
        ano = datetime.now().year

    if request.vars["exportar"] == "True":
        redirect(URL('services','exportarEstadisticas',vars=dict(mes=mes,ano=ano)))

    # Varbiales estadisticas
    cantidadTotal = 0
    duracionTotal = 0
    duracionPromedio = 0
    estadisticas = dict.fromkeys(["CM","AME1","AME2","IDE","IDV","PC","AY","MP","RES1","RES2","SE","GP","NSA","FA"],0)

    # Servicios aprobados
    servicios = db(db.servicio.aprobado == True).select()
    for servicio in servicios:

        mesServicio = datetime.strptime(servicio.fechaCreacion, "%d/%m/%Y").month
        anoServicio = datetime.strptime(servicio.fechaCreacion, "%d/%m/%Y").year

        if (mes=="0" or mesServicio == int(mes)) and anoServicio == int(ano):

            # Contador de tipo de servicio aumenta en 1
            estadisticas[servicio.tipo]+=1

            duracionServicio = obtenerDuracionServicio(servicio)

            cantidadTotal += 1
            duracionTotal += duracionServicio

    if cantidadTotal == 0:
        cantidadTotal = 1

    duracionPromedio = duracionTotal / cantidadTotal

    return dict(estadisticas=estadisticas,mes=obtenerNombreMes(mes),ano=ano,duracionPromedio=duracionPromedio,duracionTotal=duracionTotal)

# Obtener tipo de afectado de un servicio
def obtenerTipoAfectado(tipo):
    if tipo == '1':
        return "Estudiante de la USB"
    if tipo == '2':
        return "Profesor de la USB"
    if tipo == '3':
        return "Empleado de la USB"
    if tipo == '4':
        return "Obrero de la USB"
    if tipo == '5':
        return "Externo"
    return "None"

# Vista para generar exportacion de estadisticas
def exportarServicio():

    serviceId = request.vars["id"]
    # Info basica del servicio
    service = db(db.servicio.id == serviceId).select()[0]

    # Comisiones del servicio
    comisiones = obtenerComisiones(serviceId)

    # Afectados del servicio
    afectados = obtenerAfectados(serviceId)

    for afectado in afectados:
        afectado["tipo"] = obtenerTipoAfectado(afectado["tipo"])

    # Comisiones de apoyos
    externos = obtenerApoyoExterno(serviceId)

    return dict(id = serviceId, servicio = service, comisiones = comisiones, afectados = afectados, externos = externos)

def exportarEstadisticas():
    # Mes solicitado para mostrar estadisticas de servicios
    mes = request.vars['mes']
    if mes == None:
        mes = "0"

    # Ano solicitado para mostrar estadisticas de servicios
    ano = request.vars['ano']
    if ano == None:
        ano = datetime.now().year

    # Varbiales estadisticas
    cantidadTotal = 0
    duracionTotal = 0
    duracionPromedio = 0
    estadisticas = dict.fromkeys(["CM","AME1","AME2","IDE","IDV","PC","AY","MP","RES1","RES2", "SE", "GP","NSA","FA"],0)

    # Servicios aprobados
    servicios = db(db.servicio.aprobado == True).select()
    for servicio in servicios:

        mesServicio = datetime.strptime(servicio.fechaCreacion, "%d/%m/%Y").month
        anoServicio = datetime.strptime(servicio.fechaCreacion, "%d/%m/%Y").year

        if (mes=="0" or mesServicio == int(mes)) and anoServicio == int(ano):

            # Contador de tipo de servicio aumenta en 1
            estadisticas[servicio.tipo]+=1

            duracionServicio = obtenerDuracionServicio(servicio)

            cantidadTotal += 1
            duracionTotal += duracionServicio

    if cantidadTotal == 0:
        cantidadTotal = 1

    duracionPromedio = duracionTotal / cantidadTotal

    return dict(estadisticas=estadisticas,mes=obtenerNombreMes(mes),ano=ano,duracionPromedio=duracionPromedio,duracionTotal=duracionTotal)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Otras funciones
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@cache.action()
@auth.requires_login()
def download():
    """
    allows downloading of uploaded files
@auth.requires_login()
http://..../[app]/
    default/download/[filename]
    """
    return response.download(request, db)


@auth.requires_login()
def call():
    """
    exposes services. for example:
@auth.requires_login()
http://..../[app]/
    default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
