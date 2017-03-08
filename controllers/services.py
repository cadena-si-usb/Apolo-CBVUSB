# -*- coding: utf-8 -*-
from gluon.serializers import json

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman las vistas de "Mis servicios"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista principal de "Mis Servicios"
def myservices():
    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db().select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Vista para listar "Mis servicios aprovados"
def msapproved():
    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db(db.servicio.Aprueba != None).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Vista para listar "Mis servicios pendientes por aprovación"
def mspending():
    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db((db.servicio.Aprueba == None) & (db.servicio.Borrador == False)).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Vista para listar "Mis servicios guardados en borradores"
def msdraft():
    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db(db.servicio.Borrador == True).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Botón para eliminar un servicio en cualquier vista de "Mis servicios"
def deleteMyService():
    serviceId = request.vars.row_id
    db(db.servicio.id == serviceId).delete()
    redirect(URL('services','myservices'))

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman las vistas de "Gestionar servicios"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista principal de "Gestionar Servicios"
def allservices():
    services = db(db.servicio.Borrador == False).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Vista para listar "Todos los servicios aprobados"
def asapproved():
    services = db(db.servicio.Aprueba != None).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Vista para listar "Todos los servicios pendientes por aprobación"
def aspending():
    services = db((db.servicio.Aprueba == None) & (db.servicio.Borrador == False)).select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

# Botón para eliminar un servicio en cualquier vista de "Gestionar servicios"
def deleteService():
    serviceId = request.vars.row_id
    db(db.servicio.id == serviceId).delete()
    redirect(URL('services','allservices'))

# Vista para visualizar servicio
def displayService():
    serviceId = request.vars.id
    service = db(db.servicio.id == serviceId).select()[0]
    return dict(service=service)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista principal (Servicios)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista principal de "Servicios"
def index():
    services = db().select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Buscar servicios"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista principal de "Buscar servicios"
def search(): return dict()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Registrar servicio"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtener nombres de bomberos para autocompletado de registro de comisiones
def obtenerNombreBomberos():
    bomberos = db(db.bombero.id_persona == db.persona.id).select()
    nombreBomberos = list()
    for bombero in bomberos:
        nombreBomberos.append(  bombero.persona.primer_nombre    + " " +\
                                bombero.persona.segundo_nombre   + " " +\
                                bombero.persona.primer_apellido  + " " +\
                                bombero.persona.segundo_apellido)
    return nombreBomberos

def registrarComisiones(request):

    commissionCounter = 1

    # Procesar cada comision agregada
    while request.vars["comissionTitle"+str(commissionCounter)] is not None:
        
        # Jefe de comision
        jefeComision = request.vars["commissionBoss"+str(commissionCounter)]
        
        # Acompanantes
        acompanantesCounter = 1
        acompanantes = list()
        while request.vars["comissionMember"+str(commissionCounter)+"-"+str(acompanantesCounter)] is not None:
            acompanantes.append(request.vars["comissionMember"+str(commissionCounter)+"-"+str(acompanantesCounter)])
            acompanantesCounter+=1

        # Unidades
        UnidadesCounter = 1
        unidades = list()
        conductores = list()
        while request.vars["unitValue"+str(commissionCounter)+"-"+str(UnidadesCounter)] is not None:
            unidades.append(request.vars["unitValue"+str(commissionCounter)+"-"+str(UnidadesCounter)])
            conductores.append(request.vars["comissionDriver"+str(commissionCounter)+"-"+str(UnidadesCounter)])
            UnidadesCounter+=1

        commissionCounter+=1

# Vista principal de "Registrar servicio"
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
        fechaCreacion = request.vars['fechaCreacion']
        fechaLlegada = request.vars['fechaLlegada']
        fechaFinalizacion = request.vars['fechaFinalizacion']
        descripcionServicio = request.vars['descripcion']
        localizacionServicio = request.vars['localizacion']

        # Registrar datos de comisiones asociadas
        registrarComisiones(request)

        insertarServicio(fechaCreacion,fechaLlegada,fechaFinalizacion,descripcionServicio,localizacionServicio,tipoServicio,borrador)

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

        return dict(nuevoServicioId=ultimoServicioId + 1, nombreBomberos=nombreBomberos)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista de "Editar borrador"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
# Otras funciones
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
