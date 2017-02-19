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
        
        tipoServicio = request.vars['tipo'] 
        fechaCreacion = request.vars['fechaCreacion']
        fechaLlegada = request.vars['fechaLlegada']
        fechaFinalizacion = request.vars['fechaFinalizacion']
        descripcionServicio = request.vars['descripcion']
        localizacionServicio = request.vars['localizacion']
    
        insertarServicio(fechaCreacion,fechaLlegada,fechaFinalizacion,descripcionServicio,localizacionServicio,tipoServicio)
        redirect(URL('services','index.html'))
    return dict()


def services(): 

    services = db().select(orderby=~db.servicio.fechaCreacion)
    return dict(services=services)

def deleteService():

    #serviceId = 1
    #db(db.servicio.id == serviceId)._delete()
    return dict()

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

