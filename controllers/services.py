# -*- coding: utf-8 -*-

def myservices():

    # bombero_carnet = request
    #servicios = db(db.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = db().select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)
    ##################################################

def register():

    # Cada request.vars['algo'] depende de como lo hallan llamado en el form en html
    if request.env.request_method == 'POST':
        
        print request.vars['id']

        tipoServicio = request.vars['tipo'] 
        fechaCreacion = request.vars['fechaCreacion']
        fechaLlegada = request.vars['fechaLlegada']
        fechaFinalizacion = request.vars['fechaFinalizacion']
        descripcionServicio = request.vars['descripcion']
        localizacionServicio = request.vars['localizacion']
    
        insertarServicio(fechaCreacion,fechaLlegada,fechaFinalizacion,descripcionServicio,localizacionServicio,tipoServicio)
        redirect(URL('services','index.html'))

    else:
        # Obtener ID de ultimo servicio registrado
        # ID de nuevo servicio sera ultimo ID + 1
        ultimoServicioId = db.servicio.id.max()
        ultimoServicioId = db().select(ultimoServicioId).first()[ultimoServicioId]
        
        # Caso especial para 1er servicio registrado
        if ultimoServicioId is None:
            ultimoServicioId = 0

        return dict(nuevoServicioId=ultimoServicioId + 1)


def services(): 

    services = db().select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

def deleteService():

    serviceId = request.vars.row_id
    db(db.servicio.id == serviceId).delete()
    redirect(URL('services','services'))

def deleteMyService():
    serviceId = request.vars.row_id
    db(db.servicio.id == serviceId).delete()
    redirect(URL('services','myservices'))

def index(): return dict()
def search(): return dict()


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

