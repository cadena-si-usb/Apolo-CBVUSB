# -*- coding: utf-8 -*-

def myServices():

    # bombero_carnet = request
    #servicios = DB(DB.bombero.carnet == bombero_carnet)._select()
    #return dict(servicios=servicios)

    ### MIENTRAS TANTO MOSTRAR TODOS LOS SERVICIOS ###
    services = DB().select(DB.servicio.ALL)
    return dict(services=services)
    ##################################################

def register():

    form = SQLFORM(DB.servicio)
    
    #print form

    return dict()


def services(): 

    services = DB().select(DB.servicio.ALL)
    return dict(services=services)

def deleteService():

    #serviceId = 1
    #DB(DB.servicio.id == serviceId)._delete()
    return dict()


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, DB)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
