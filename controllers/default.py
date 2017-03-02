# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def indexno():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

def perfilth():
    usuario = db(db.persona.id==str(1)).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id))
    
    return dict(usuario=usuario)

def perfilmodth():

    form = SQLFORM(db.persona)

    if form.process(session=None, formname='test').accepted:
        response.flash = 'La modificación fue exitosa.'
    elif form.errors:
        response.flash = 'La modificación fue errónea.'
    else:
        response.flash = 'Complete el formulario de modificación.'

    return dict(form=form)

def registrousrth():

    exito = True

    formUsuario = SQLFORM(db.usuario)
    formPersona = SQLFORM(db.persona)
    formBombero = SQLFORM(db.bombero)

    if (formUsuario.process(session=None, formname='Usuario').accepted and
        formPersona.process(session=None, formname='Persona').accepted and
        formBombero.process(session=None, formname='Bombero').accepted):
        pass
    elif formUsuario.errors or formPersona.errors or formBombero.errors:
        exito = False

    if exito:
        response.flash = '¡El usuario '+str(formUsuario)+' ha sido registrado exitosamente!'
    else:
        response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'

    return dict(formUsuario=formUsuario, formPersona=formPersona, formBombero=formBombero)

def buscarth():
    busqueda = request.vars.getlist("buscar")
    
    if busqueda != [] :
        # Busca por iniciales, nombres, apellidos y username, sin importar que la palabra este en mayuscula o minuscula
        # ilike es case insensitive
        palabra = str(busqueda[0]) + '%'
        tabla = db(
                    db.persona.primer_nombre.ilike(palabra)|
                    db.persona.segundo_nombre.ilike(palabra)|
                    db.persona.primer_apellido.ilike(palabra)|
                    db.persona.segundo_apellido.ilike(palabra)|
                    db.usuario.username.ilike(palabra)|
                    db.bombero.iniciales.ilike(palabra)
                    ).select(
                            join=db.bombero.on(
                                                (db.bombero.id_persona == db.persona.id) & 
                                                (db.persona.id == db.usuario.id) & 
                                                (db.bombero.id == db.usuario.id)),
                            distinct=db.persona.id)
    else:
        tabla = db(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id))

    return dict(tabla=tabla)
    
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


## Inician nuestras funciones
