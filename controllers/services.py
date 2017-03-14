# -*- coding: utf-8 -*-
from gluon.serializers import json
from datetime import datetime
#from emailManager import emailManager
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
    services = db(((db.servicio.Borrador == False) & db.servicio.Aprueba == None)).select(orderby=~db.servicio.fechaCreacion)
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

# Vista para visualizar servicio
@auth.requires_login()
def displayService():
    serviceId = request.vars.id
    service = db(db.servicio.id == serviceId).select()[0]
    return dict(service=service)

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
            personaID = db(db.persona.cedula == cedulaAfectado).select().first()["id"]
        except:
            personaID = None

        # Registrar como afectado
        db.es_afectado.insert(
            servicio = request.vars["id"],
            persona = personaID,
            notastratamiento = notasYtratamiento,
            tipo = tipoAfectado)

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

        # Registrar como afectado
        db.comision_apoyo.insert(
            numeroacompanantes = numAcompanantes,
            cuerpoodepartamento = cuerpoDeptExt,
            unidad = unitExt,
            placaunidad = unitExtPlaca,
            lider = 1, # ?????? No esta campo en form
            servicio = request.vars["id"])

        comisionCounter+=1

@auth.requires_login()
def convertDateTime(fecha, hora):
    return datetime.strptime(fecha + " " + hora, '%m/%d/%Y %I:%M%p')

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
        fechaFinalizacion = request.vars['fechaFinalizacion']
        horaFinalizacion = request.vars['horaFinalizacion']
        descripcionServicio = request.vars['descripcion']
        localizacionServicio = request.vars['localizacion']

        # Registrar servicio
        fechaCreacion = convertDateTime(fechaCreacion,horaCreacion)
        #fechaLlegada = convertDateTime(fechaLlegada,horaLlegada)
        fechaFinalizacion = convertDateTime(fechaFinalizacion,horaFinalizacion)
        insertarServicio(fechaCreacion,fechaLlegada,fechaFinalizacion,descripcionServicio,localizacionServicio,tipoServicio,borrador)

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
        servicio.fechaCreacion = request.vars['fechaCreacion']
        servicio.fechaLlegada = request.vars['fechaLlegada']
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

        return dict(service=service, nombreBomberos=nombreBomberos)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Aprobar Servicio"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@auth.requires_login()
def aprove():
    services = db(db.servicio.Aprueba != None).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

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
