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
    redirect(URL('services','services'))

# Vista para visualizar servicio
def displayService():
    serviceId = request.vars.id
    service = db(db.servicio.id == serviceId).select()[0]
    return dict(service=service)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman la vista principal (Servicios)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Vista principal de "Servicios"
def index(): return dict()

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

# Vista principal de "Registrar servicio"
def register():
    # Cada request.vars['algo'] depende de como lo hallan llamado en el form en html
    if request.env.request_method == 'POST':

        print request.vars["jefeComision"]
        print request.vars["conductor"]
        print request.vars["acompanante"]

        #tipoServicio = request.vars['tipo']
        #fechaCreacion = request.vars['fechaCreacion']
        #fechaLlegada = request.vars['fechaLlegada']
        #fechaFinalizacion = request.vars['fechaFinalizacion']
        #descripcionServicio = request.vars['descripcion']
        #localizacionServicio = request.vars['localizacion']

        #insertarServicio(fechaCreacion,fechaLlegada,fechaFinalizacion,descripcionServicio,localizacionServicio,tipoServicio)
        #redirect(URL('services','index.html'))

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

        servicio.update_record()

        redirect(URL('services','index.html'))

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
