# -*- coding: utf-8 -*-
from gluon.serializers import json
from datetime import datetime
#from emailManager import emailManager Mientras no se use esta comentado xD

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman las vistas de "Mis servicios"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista para listar "Mis servicios aprovados"
@auth.requires_login()
def msapproved():
    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db(db.servicio.Aprueba != None).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Vista para listar "Mis servicios pendientes por aprovación"
@auth.requires_login()
def mspending():
    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db((db.servicio.Borrador == False) & (db.servicio.Aprueba == None)).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Vista para listar "Mis servicios guardados en borradores"
@auth.requires_login()
def msdraft():
    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db((db.servicio.Borrador == True) & (db.servicio.Aprueba == None)).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

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
    services = db(db.servicio.Aprueba != None).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Vista para listar "Mis Servicios"
@auth.requires_login()
def myservices():
    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db(db.servicio.Aprueba != None).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

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

        # Jefe de comision
        bomberoRow = db(db.bombero.id == comisionRow.lider).select()[0]
        comision['jefe'] = nombreBombero(bomberoRow.id_persona)       

        # Unidad
        unidadUtilizadaRow = db(db.unidad_utilizada_por.comision == comisionRow.id).select()[0]
        if unidadUtilizadaRow.unidad is None:
            comision["unidad"] = None
        else:
            unidadRow = db(db.unidad.id == unidadUtilizadaRow.unidad).select()[0]
            comision["unidad"] = unidadRow.nombre
            bomberoRow = unidadUtilizadaRow.conductor
            comision["conductor"] = nombreBombero(bomberoRow.id_persona)

        # Acompanantes
        acompanantes = list()
        esAcompananteSet = db(db.es_acompanante.comision == comisionRow.id).select()
        for esAcompananteRow in esAcompananteSet:
            bomberoRow = esAcompananteRow.bombero
            nombre = nombreBombero(bomberoRow.id_persona)
            acompanantes.append(nombre)

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
            afectado["numeros"].append(str(numeroRow.codigo_telefono)+"-"+str(numeroRow.numero_telefono))

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
    services = db(db.servicio.Aprueba != None).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

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

    commissionCounter = 1
    idBomberos = obtenerNombreBomberos()
    idUnidades = obtenerNombreUnidades()

    # Procesar cada comision agregada
    while request.vars["commissionTitle"+str(commissionCounter)] is not None:

        # Jefe de comision
        jefeComision = request.vars["commissionBoss"+str(commissionCounter)]

        # Acompanantes
        acompanantesCounter = 1
        acompanantes = list()
        while request.vars["commissionMember"+str(commissionCounter)+"-"+str(acompanantesCounter)] is not None:
            acompanantes.append(request.vars["commissionMember"+str(commissionCounter)+"-"+str(acompanantesCounter)])
            acompanantesCounter+=1

        # Unidades
        UnidadesCounter = 1
        unidades = list()
        conductores = list()
        while request.vars["unitValue"+str(commissionCounter)+"-"+str(UnidadesCounter)] is not None:
            unidades.append(request.vars["unitValue"+str(commissionCounter)+"-"+str(UnidadesCounter)])
            conductores.append(request.vars["commissionDriver"+str(commissionCounter)+"-"+str(UnidadesCounter)])
            UnidadesCounter+=1

        commissionCounter+=1

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

    affectedCounter = 1

    # Procesar cada afectado agregado
    while request.vars["affectedTitle"+str(affectedCounter)] is not None:

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
        try:
            personaID = db(db.persona.cedula == cedulaAfectado).select()[0]["id"]
        except:
            personaID = None

        # Registrar como afectado
        db.es_afectado.insert(
            servicio = request.vars["id"],
            persona = personaID,
            notastratamiento = notasYtratamiento,
            tipo = tipoAfectado)

        # Telefonos
        telfCounter = 1
        while request.vars["affectedPhone"+str(affectedCounter)+"-"+str(telfCounter)] is not None:
            request.vars["affectedPhone"+str(affectedCounter)+"-"+str(telfCounter)]
            telf = request.vars["affectedPhone"+str(affectedCounter)+"-"+str(telfCounter)].split("-")
            telf.append("")
            db.numero.insert(
                id_persona = personaID,
                codigo_telefono = telf[0],
                numero_telefono = telf[1])
            telfCounter += 1

        affectedCounter+=1

@auth.requires_login()
def registrarApoyoExterno(request):

    comisionCounter = 1

    # Procesar cada afectado agregado
    while request.vars["comisionExtTitle"+str(comisionCounter)] is not None:

        cuerpoDeptExt = request.vars["cuerpoDepartamento"+str(comisionCounter)]
        numAcompanantes = request.vars["numAcomp"+str(comisionCounter)]

        unitExt = request.vars["unitExtValue"+str(comisionCounter)+"-1"]
        unitExtPlaca = request.vars["unitExtPlaca"+str(comisionCounter)+"-1"]

        jefe = request.vars["jefe"+str(comisionCounter)]
        # comentario = request.vars["comentario"+str(comisionCounter)]

        # Registrar como afectado
        db.comision_apoyo.insert(
            numeroacompanantes = numAcompanantes,
            cuerpoodepartamento = cuerpoDeptExt,
            unidad = unitExt,
            placaunidad = unitExtPlaca,
            lider = jefe,
            comentario = "PENDIENTE",
            servicio = request.vars["id"])

        comisionCounter+=1

# Vista principal de "Registrar servicio"
@auth.requires_login()
def register():

   # Form rellenado y submiteado por usuario
    if request.env.request_method == 'POST':

        # Guardar borrador de form
        if request.vars['draft'] is not None:
            borrador = True
        # Registrar form completo
        else:
            borrador = False

        tipoServicio = request.vars['tipo']
        horaCreacion = request.vars['horaCreacion']
        fechaCreacion = request.vars['fechaCreacion']
        horaLlegada = request.vars['horaLlegada']
        fechaLlegada = request.vars['fechaLlegada']
        horaFinalizacion = request.vars['horaFinalizacion']
        fechaFinalizacion = request.vars['fechaFinalizacion']
        descripcionServicio = request.vars['descripcion']
        localizacionServicio = request.vars['localizacion']
        
        insertarServicio(horaCreacion,fechaCreacion,horaFinalizacion,fechaFinalizacion,descripcionServicio,localizacionServicio,tipoServicio,borrador)

        # Registrar datos de comisiones, afectados y apoyo externo
        registrarComisiones(request)
        registrarAfectados(request)
        registrarApoyoExterno(request)

        # Borrador guardado. Redireccionar a edicion de borrador para continuar con registro
        if request.vars['draft'] is not None:
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

        return dict(nuevoServicioId=ultimoServicioId + 1, nombreBomberos=nombreBomberos, nombreUnidades=nombreUnidades)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Editar borrador"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

        # Registrar form
        if request.vars['draft'] is None:
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

        return dict(service=service, nombreBomberos=nombreBomberos, comisiones=comisiones, afectados=afectados, externos=externos)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Aprobar Servicio"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@auth.requires_login()
def aprove():
    services = db(db.servicio.Aprueba != None).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)


# Vista de "Estadisticas"
def stadistics():
    return dict()


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
