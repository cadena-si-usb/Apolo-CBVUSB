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
	T.force('es')
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
	T.force('es')
	userid = auth.user.id
	bombero=db(db.bombero.id_usuario==userid).select().first()
	persona=db(db.persona.id==bombero.id_persona).select().first()
	usuario=db(db.usuario.id==userid).select().first()
	tipo=""

	formUsuario = SQLFORM.factory(
		Field('password', 
			type='password', 
			notnull=True, 
			default=usuario.password, 
			requires=[IS_MATCH('^[\w~!@#$%^&*\-+=`|(){}[\]<>\.\?\/]{4,24}$', error_message='La contraseña debe: \n'+
																								'\n\t- Contener cualquiera de los siguientes caracteres: a-z A-Z 0-9 _!@#$%^&*\-+=`|(){}[]<>.?/'+
																								'\n\t- Debe tener una longitud entre 4 y 24 caracteres.'),
						CRYPT()]
						,
			label='Clave'))
	
	if formUsuario.process(session=None, formname='perfilmodUsuario', keepvalues=True).accepted:
		print db(db.usuario.id==userid).select()
		print (formUsuario.vars)
		db(db.usuario.id==userid).update(**db.usuario._filter_fields(formUsuario.vars))
		response.flash = 'Cambio de contraseña realizado satisfactoriamente'
		tipo="success"
	elif formUsuario.errors:
		response.flash = 'Hay un error en un campo'
		tipo="danger"

	formPersona = SQLFORM.factory(
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
			)
		)
	
	if formPersona.process(session=None, formname='perfilmodPersona', keepvalues=True).accepted:
		db(db.persona.id==bombero.id_persona).update(**db.persona._filter_fields(formPersona.vars))
		response.flash = 'Cambio realizado satisfactoriamente'
		tipo="success"
	elif formPersona.errors:
		response.flash = 'Hay un error en un campo'
		tipo="danger"

	formBombero = SQLFORM.factory(
		Field('cargo', 
			type='string', 
			notnull=True, 
			default=bombero.cargo,
			requires = IS_IN_SET(['Administrador', 'Comandante en Jefe', 'Primer comandante', 'Segundo comandante', 
									'Inspector en Jefe', 'sub-Inspector',
									'Gerente de Riesgo', 'Gerente de Administración', 'Gerente de Educación', 'Gerente de Operaciones','Gerente de Talento humano',
									'Coordinador de Riesgo', 'Coordinador de Administración', 'Coordinador de Educación', 'Coordinador de Operaciones','Coordinador de Talento humano',
									'Miembro de Riesgo', 'Miembro de Administración', 'Miembro de Educación', 'Miembro de Operaciones','Miembro de Talento humano',
									'Estudiante'], error_message='Debe seleccionar una opción')))
	
	if formBombero.process(session=None, formname='perfilmodBombero', keepvalues=True).accepted:
		db(db.bombero.id_usuario==userid).update(**db.bombero._filter_fields(formBombero.vars))
		user = db(db.bombero.id==userid).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id)).first()
		response.flash = 'Cambio realizado satisfactoriamente'
		tipo="success"
	elif formBombero.errors:
		response.flash = 'Hay un error en un campo'
		tipo="danger"


	return dict(formBombero=formBombero,formPersona=formPersona,formUsuario=formUsuario,tipo=tipo)	

# DEBO CONSIDERAR EL NONE! Si es None colocar entonces ''
def registrousrth1():
	T.force('es')
	tipo=""
	formPersona = SQLFORM.factory(
		Field('username', 
				type='string', 
				length=512, 
				unique=True, 
				requires=[IS_MATCH('^\w{6,16}', 
								error_message='El nombre de usuario debe:'+
												'\n\t- Contener unicamente los caracteres: a-z, A-Z, 0-9 y _'+
												'\n\t- Debe tener una longitud de entre 6 y 16 caracteres.'),
							IS_NOT_IN_DB(db, db.usuario.username, 
								error_message='Ya existe un usuario con ese nombre.')],
				label='Nombre de usuario'),
		Field('password', 
				type='password', 
				readable=False, 
				length=512, 
				requires=[IS_MATCH('^[\w~!@#$%^&*\-+=`|(){}[\]<>\.\?\/]{4,24}$', 
								error_message='La contraseña debe: \n'+
												'\n\t- Contener cualquiera de los siguientes caracteres: a-z A-Z 0-9 _!@#$%^&*\-+=`|(){}[]<>.?/'+
												'\n\t- Debe tener una longitud entre 4 y 24 caracteres.'),
							CRYPT()],
				label='Clave'),
		Field('cedula_letra', 
				type='string', 
				length=512, 
				unique=True, 
				requires=[IS_IN_SET(['V','E'], 
								error_message='No es una opción válida')],
				label='Nacionalidad'),
		Field('cedula', 
				type='string',
				length=512, 
				requires=[IS_INT_IN_RANGE(minimum=1,maximum=100000000, 
								error_message='Numero de cedula no valido')],
				label='Cédula'),
		Field('primer_nombre', 
				type='string',
				length=512, 
				requires=[IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', 
								error_message='Debe contener sólo carácteres')],
				label='Primer nombre'),
		Field('segundo_nombre',
				type='string',
				length=512, 
				requires=[IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', 
								error_message='Debe contener sólo carácteres'))],
				label='Primer nombre'),
		Field('primer_apellido',
				type='string',
				length=512, 
				requires=[IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', 
								error_message='Debe contener sólo carácteres')],
				label='Primer nombre'),
		Field('segundo_apellido',
				type='string',
				length=512, 
				requires=[IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', 
								error_message='Debe contener sólo carácteres'))],
				label='Primer nombre'),
		Field('fecha_nacimiento',
				type='date',
				requires=[IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')]),
		Field('lugar_nacimiento'),
		Field('genero'),
		Field('imagen'),
		Field('email_principal'),
		Field('email_alternativo'),
		Field('estado_civil') 
		)

	if formPersona.process(session=None, formname='Persona', keepvalues=True).accepted:
		formPersona.vars = dict((k,v) for k,v in formPersona.vars.iteritems() if v is not None)
		redirect(URL("default","registrousrth2",vars=formPersona.vars))

	elif formPersona.errors:
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'
		tipo="danger"

	return dict(formPersona=formPersona,tipo=tipo)

def registrousrth2():

	usuario=db.usuario._filter_fields(request.vars)
	persona=db.persona._filter_fields(request.vars)
	tipo=""

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

		response.flash = '¡El usuario '+str(db.usuario[id_usuario].username)+' ha sido registrado satisfactoriamente!'
		tipo= "success"

	elif formBombero.errors:
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'
		tipo="danger"

	return dict(formBombero=formBombero,tipo=tipo)

def eliminarusrth():
	tipo = ""
	
	if request.args:
		
		id_bombero = int(request.args[0])
		
		if not db(db.bombero.id==id_bombero).isempty():
			bombero = db(db.bombero.id==id_bombero).select().first()
			username = str(db.usuario[bombero.id_usuario].username)
			id_usuario = bombero.id_usuario
			id_persona = bombero.id_persona
			db(db.persona.id==id_persona).delete()
			db(db.usuario.id==id_usuario).delete()
			response.flash = '¡El usuario '+username+' ha sido eliminado satisfactoriamente!'
			tipo = "success"


	tabla = db(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id),orderby=~db.bombero.carnet)

	if len(tabla) == 0:
		response.flash = 'No hay usuarios en el sistema.'
		tipo="warning"

	return dict(tabla=tabla,tipo=tipo)

#@auth.requires_login()
def buscarth():
	# Busqueda suministrada por el usuario
	busqueda = request.vars.getlist("buscar")
	error = False
	tipo=""

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
								distinct=db.bombero.carnet,
								orderby=~db.bombero.carnet) # =~ se refiere al orden descendente

			if len(tabla) == 0:
				error = True
		else:
			error = True
	else:
		tabla = db(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id),orderby=~db.bombero.carnet)

	if error:
		if busqueda[0] != '':
			response.flash = 'No hay registro para esta búsqueda.'
			tipo="danger"
		tabla = db(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id),orderby=~db.bombero.carnet)

	return dict(tabla=tabla,tipo=tipo)
	
@cache.action()
def download():
	"""
	allows downloading of uploaded files
	http://..../[app]/default/download/[filename]
	"""
	return response.download(request, db)

@auth.requires_login()
def call():
	"""
	exposes services. for example:
	http://..../[app]/default/call/jsonrpc
	decorate with @services.jsonrpc the functions to expose
	supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
	"""
	return service()


## Inician nuestras funciones
