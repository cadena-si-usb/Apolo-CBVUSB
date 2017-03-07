# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#psql -U cbvusb -h localhost -W

import re
import time

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
	return dict()

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

@auth.requires_login()
def perfilth():

	if request.args:
		userid = int(request.args[0])
	else:
		userid = auth.user.id

	usuario = db(db.bombero.id==userid).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id)).first()
	
	return dict(usuario=usuario)

@auth.requires_login()
def perfilmodth():

	userid = auth.user.id
	bombero=db(db.bombero.id_usuario==userid).select().first()
	persona=db(db.persona.id==bombero.id_persona).select().first()

	form = SQLFORM.factory(
		Field('cedula', 
			type='string', 
			unique=True, 
			default=persona.cedula, 
			requires=IS_MATCH('^[VE]-\d+$', error_message='Debe tener un formato válido V-XXXXXXX o E-XXXXXXXX')
			),
		Field('primer_nombre', 
			type='string', 
			notnull=True, 
			default=persona.primer_nombre, 
			requires=IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
			),
		Field('segundo_nombre', 
			type='string',
			default=persona.segundo_nombre, 
			requires=IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres'))
			),
		Field('primer_apellido', 
			type='string', 
			notnull=True,
			default=persona.primer_apellido, 
			requires=IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
			),
		Field('segundo_apellido', 
			type='string',
			default=persona.segundo_apellido, 
			requires=IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres'))
			),
		Field('fecha_nacimiento', 
			type='date', 
			notnull=True,
			default=persona.fecha_nacimiento,
			requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
			),
		Field('lugar_nacimiento', 
			type='string', 
			notnull=True,
			default=persona.lugar_nacimiento, 
			requires=IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
			),
		Field('genero', 
			type='string', 
			notnull=True,
			default=persona.genero, 
			requires=IS_IN_SET(['Masculino','Femenino'], error_message='No es una opción válida')
			),
		Field('imagen', type='text',
			default=persona.imagen
			),
		Field('email_principal', 
			type='string', 
			notnull=True,
			default=persona.email_principal, 
			requires=IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com')
			),
		Field('email_alternativo', 
			type='string',
			default=persona.email_alternativo, 
			requires=IS_EMPTY_OR(IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'))
			),
		Field('estado_civil', 
			type='string', 
			notnull=True,
			default=persona.estado_civil, 
			requires=IS_IN_SET(['Soltero','Casado','Divorciado','Viudo'], error_message='No es una opción válida')
			),
		Field('tipo_sangre', 
			type='string', 
			notnull=True,
			default=bombero.tipo_sangre,
			requires=IS_IN_SET(['A+','A-','B+','B-','AB+','AB-','O+','O-'], error_message='Debe ser alguno de los tipos válidos')
			),
		Field('cargo', 
			type='string', 
			notnull=True, 
			default=bombero.cargo,
			requires = IS_IN_SET(['Administrador', 'Comandante en Jefe', 'Primer comandante', 'Segundo comandante', 
									'Inspector en Jefe', 'sub-Inspector',
									'Gerente de Riesgo', 'Gerente de Administración', 'Gerente de Educación', 'Gerente de Operaciones','Gerente de Talento humano',
									'Coordinador de Riesgo', 'Coordinador de Administración', 'Coordinador de Educación', 'Coordinador de Operaciones','Coordinador de Talento humano',
									'Miembro de Riesgo', 'Miembro de Administración', 'Miembro de Educación', 'Miembro de Operaciones','Miembro de Talento humano',
									'Estudiante'], error_message='Debe seleccionar una opción'))
		)

	if form.process(session=None, formname='perfilmod', keepvalues=True).accepted:
		db(db.bombero.id_usuario==userid).update(**db.bombero._filter_fields(form.vars))
		db(db.persona.id==bombero.id_persona).update(**db.persona._filter_fields(form.vars))

	elif form.errors:
		response.flash = 'Hay un error en un campo'

	return dict(form=form)

def registrousrth():
	formUsuario = SQLFORM(db.usuario)
	formPersona = SQLFORM(db.persona)
	formBombero = SQLFORM(db.bombero)

	if (formUsuario.process(session=None, formname='Usuario').accepted and
		formPersona.process(session=None, formname='Persona').accepted and
		formBombero.process(session=None, formname='Bombero').accepted):
		response.flash = '¡El usuario '+str(formUsuario)+' ha sido registrado exitosamente!'

	elif formUsuario.errors or formPersona.errors or formBombero.errors:
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'

	return dict(formUsuario=formUsuario, formPersona=formPersona, formBombero=formBombero)

# DEBO CONSIDERAR EL NONE! Si es None colocar entonces ''
def registrousrth1():
	formPersona = SQLFORM.factory(
		Field('username', type='string', length=512, unique=True, requires=[IS_MATCH('^\w{6,16}', error_message='El nombre de usuario debe:'+
																	'\n\t- Contener unicamente los caracteres: a-z, A-Z, 0-9 y _'+
																	'\n\t- Debe tener una longitud de entre 6 y 16 caracteres.'),
								IS_NOT_IN_DB(db, db.usuario.username, error_message='Ya existe un usuario con ese nombre.')]),
		Field('password', type='password', readable=False, length=512, requires=[IS_MATCH('^[\w~!@#$%^&*\-+=`|(){}[\]<>\.\?\/]{4,24}$', error_message='La contraseña debe: \n'+
																										'\n\t- Contener cualquiera de los siguientes caracteres: a-z A-Z 0-9 _!@#$%^&*\-+=`|(){}[]<>.?/'+
																										'\n\t- Debe tener una longitud entre 4 y 24 caracteres.'),
								CRYPT()]), 
		db.persona)

	if formPersona.process(session=None, formname='Persona', keepvalues=True).accepted:
		formPersona.vars = dict((k,v) for k,v in formPersona.vars.iteritems() if v is not None)
		redirect(URL("default","registrousrth2",vars=formPersona.vars))

	elif formPersona.errors:
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'

	return dict(formPersona=formPersona)

def registrousrth2():

	usuario=db.usuario._filter_fields(request.vars)
	persona=db.persona._filter_fields(request.vars)

	formBombero = SQLFORM.factory(
		Field('carnet', type='integer', unique=True, requires=IS_INT_IN_RANGE(0, error_message='Debe ser positivo')),
		Field('iniciales', type='string', requires=IS_EMPTY_OR(IS_LENGTH(minsize=2,maxsize=4))),
		Field('tipo_sangre', type='string', requires=IS_IN_SET(['A+','A-','B+','B-','AB+','AB-','O+','O-'], error_message='Debe ser alguno de los tipos válidos'))
		)

	if formBombero.process(session=None, formname='Bombero', keepvalues=True).accepted:

		primer_nombre=persona['primer_nombre']
		primer_apellido=persona['primer_apellido']
		email_principal=persona['email_principal']

		id_usuario=db.usuario.insert(first_name=primer_nombre, last_name=primer_apellido, email=email_principal, **usuario)		
		id_persona=db.persona.insert(**persona)

		id_bombero=db.bombero.insert(id_usuario=id_usuario, id_persona=id_persona, **db.bombero._filter_fields(formBombero.vars))

		redirect(URL("default","registrousrth_final",args=[id_usuario]))

	elif formBombero.errors:
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'

	return dict(formBombero=formBombero)

# Deseable: Que me muestre el nombre del usuario en el mensaje final
def registrousrth_final():
	id_usuario=request.args[0]
	username=db(db.usuario.id==id_usuario).select().first().username

	#redirect(URL("default","index"))
	return dict(username=username)

def eliminarusrth():
	if request.args:
		
		id_bombero = int(request.args[0])
		
		if not db(db.bombero.id==id_bombero).isempty():
			bombero = db(db.bombero.id==id_bombero).select().first()
			id_usuario = bombero.id_usuario
			id_persona = bombero.id_persona
			db(db.persona.id==id_persona).delete()
			db(db.usuario.id==id_usuario).delete()

	tabla = db(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id))

	if len(tabla) == 0:
		response.flash = 'No hay usuarios en el sistema.'

	return dict(tabla=tabla)

#@auth.requires_login()
def buscarth():
	# Busqueda suministrada por el usuario
	busqueda = request.vars.getlist("buscar")
	error = False

	if busqueda != []:
		palabra = str(busqueda[0]) + '%'
		# Expresion regular de las palabras en castellano, sin simbolos y numeros.
		regex = '[a-zA-ZñÑáéíóúÁÉÍÓÚ]+'
		if re.match(regex,palabra):
			# Query que busca todas las personas cuyo primer nombre, segundo nombre,
			# primer apellido, segundo apellido o nombre de usuario coincidan con
			# la busqueda suministrada por el usuario. Esta busqueda es case
			# insensitive
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
								distinct=db.persona.id,
								orderby=~db.bombero.carnet) # =~ se refiere al orden descendente

			if len(tabla) == 0:
				error = True
		else:
			error = True
	else:
		tabla = db(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id))

	if error:
		if busqueda[0] != None:
			response.flash = 'No hay registro para esta búsqueda.'
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
