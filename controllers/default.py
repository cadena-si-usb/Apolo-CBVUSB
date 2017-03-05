# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#psql -U cbvusb -h localhost -W

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

    if request.args:
        userid = request.args[0]
    else:
        userid = str(1)

    usuario = db(db.persona.id==userid).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id))
    
    return dict(usuario=usuario)

def perfilmodth():

    form = SQLFORM(db.persona)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
                #hay que cambiar db(db.persona.cedula==form.vars.cedula) por db.bombero.id_usuario para usos practicos 

        db(db.persona.cedula==form.vars.cedula).update(fecha_nacimiento=form.vars.fecha_nacimiento)
        db(db.persona.cedula==form.vars.cedula).update(primer_nombre=form.vars.primer_nombre)
        db(db.persona.cedula==form.vars.cedula).update(segundo_nombre=form.vars.segundo_nombre)
        db(db.persona.cedula==form.vars.cedula).update(primer_apellido=form.vars.primer_apellido)
        db(db.persona.cedula==form.vars.cedula).update(segundo_apellido=form.vars.segundo_apellido)
        db(db.persona.cedula==form.vars.cedula).update(email_principal=form.vars.email_principal)
        db(db.persona.cedula==form.vars.cedula).update(email_alternativo=form.vars.email_alternativo)
        db(db.persona.cedula==form.vars.cedula).update(imagen=form.vars.imagen)
        db(db.persona.cedula==form.vars.cedula).update(estado_civil=form.vars.estado_civil)
        db(db.persona.cedula==form.vars.cedula).update(lugar_nacimiento=form.vars.lugar_nacimiento)
        db(db.persona.cedula==form.vars.cedula).update(genero=form.vars.genero)

    elif form.errors:
        response.flash = 'Hay un error en un campo'
        
    else:
        response.flash = 'Debe completar todos los campos'

    return dict(form=form)

def registrousrth():

    """
    form = SQLFORM.factory(
        db.usuario,
        db.persona,
        db.bombero)

    
    username = request.vars.getlist("username")
    password = request.vars.getlist("password")
    cedula = request.vars.getlist("cedula")
    primer_nombre = request.vars.getlist("primer_nombre")
    segundo_nombre = request.vars.getlist("segundo_nombre")
    primer_apellido = request.vars.getlist("primer_apellido")
    segundo_apellido = request.vars.getlist("segundo_apellido")
    fecha_nacimiento = request.vars.getlist("fecha_nacimiento")
    lugar_nacimiento = request.vars.getlist("lugar_nacimiento")
    genero = request.vars.getlist("genero")
    email_principal = request.vars.getlist("email_principal")
    estado_civil = request.vars.getlist("estado_civil")
    carnet = request.vars.getlist("carnet")
    tipo_sangre = request.vars.getlist("tipo_sangre")

    if (username == [] or password == [] or cedula == [] or 
        primer_nombre == [] or segundo_nombre == [] or primer_apellido == [] or 
        segundo_apellido == [] or fecha_nacimiento == [] or 
        lugar_nacimiento == [] or genero == [] or email_principal == [] or 
        estado_civil == [] or carnet == [] or tipo_sangre == []):
        pass
    elif (username[0] == "" or password[0] == "" or cedula[0] == "" or 
        primer_nombre[0] == "" or segundo_nombre[0] == "" or 
        primer_apellido[0] == "" or segundo_apellido[0] == "" or 
        fecha_nacimiento[0] == "" or lugar_nacimiento[0] == "" or 
        genero[0] == "" or email_principal[0] == "" or estado_civil[0] == "" or 
        carnet[0] == "" or tipo_sangre[0] == ""):
        pass
    else:
        db.usuario.insert(
                            username=username[0], 
                            password=password[0])
        db.persona.insert(
                            cedula=int(cedula[0]), 
                            primer_nombre=primer_nombre[0], 
                            segundo_nombre=segundo_nombre[0], 
                            primer_apellido=primer_apellido[0], 
                            segundo_apellido=segundo_apellido[0], 
                            fecha_nacimiento=fecha_nacimiento[0], 
                            lugar_nacimiento=lugar_nacimiento[0], 
                            genero=genero[0], 
                            email_principal=email_principal[0], 
                            estado_civil=estado_civil[0])
        usuario = db(db.usuario.username==username[0]).select(db.usuario.id)[0]
        id_usuario = usuario.id
        persona = db(db.persona.cedula==cedula[0]).select(db.persona.id)[0]
        id_persona = persona.id
        db.bombero.insert(
                            carnet=int(carnet[0]), 
                            tipo_sangre=tipo_sangre[0], 
                            id_persona=id_persona, 
                            id_usuario=id_usuario)

    return dict()
    """
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
