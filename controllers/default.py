# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#psql -U cbvusb -h localhost -W

import re

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

@auth.requires_login()
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

def perfilth():

	if request.args:
		userid = int(request.args[0])
	else:
		userid = str(1)

	usuario = db(db.bombero.id==userid).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id))
	
	return dict(usuario=usuario)

def perfilmodth():

	userid = str(1)

	form = SQLFORM.factory(
		Field('cedula', 
			type='string', 
			unique=True, 
			default=db(db.persona.id==userid).select().first().cedula, 
			requires=IS_MATCH('^[VE]-\d+$', error_message='Debe tener un formato válido V-XXXXXXX o E-XXXXXXXX')
			),
		Field('primer_nombre', 
			type='string', 
			notnull=True, 
			default=db(db.persona.id==userid).select().first().primer_nombre, 
			requires=IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
			),
		Field('segundo_nombre', 
			type='string',
			default=db(db.persona.id==userid).select().first().segundo_nombre, 
			requires=IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres'))
			),
		Field('primer_apellido', 
			type='string', 
			notnull=True,
			default=db(db.persona.id==userid).select().first().primer_apellido, 
			requires=IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
			),
		Field('segundo_apellido', 
			type='string',
			default=db(db.persona.id==userid).select().first().segundo_apellido, 
			requires=IS_EMPTY_OR(IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres'))
			),
		Field('fecha_nacimiento', 
			type='date', 
			notnull=True,
			default=db(db.persona.id==userid).select().first().fecha_nacimiento,
			requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')
			),
		Field('lugar_nacimiento', 
			type='string', 
			notnull=True,
			default=db(db.persona.id==userid).select().first().lugar_nacimiento, 
			requires=IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', error_message='Debe contener sólo carácteres')
			),
		Field('genero', 
			type='string', 
			notnull=True,
			default=db(db.persona.id==userid).select().first().genero, 
			requires=IS_IN_SET(['Masculino','Femenino'], error_message='No es una opción válida')
			),
		Field('imagen', type='text',
			default=db(db.persona.id==userid).select().first().imagen
			),
		Field('email_principal', 
			type='string', 
			notnull=True,
			default=db(db.persona.id==userid).select().first().email_principal, 
			requires=IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com')
			),
		Field('email_alternativo', 
			type='string',
			default=db(db.persona.id==userid).select().first().email_alternativo, 
			requires=IS_EMPTY_OR(IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'))
			),
		Field('estado_civil', 
			type='string', 
			notnull=True,
			default=db(db.persona.id==userid).select().first().estado_civil, 
			requires=IS_IN_SET(['Soltero','Casado','Divorciado','Viudo'], error_message='No es una opción válida')
			)
		)

	if form.process(session=None, formname='perfilmod', keepvalues=True).accepted:
		db(db.persona.id==userid).update(**db.persona._filter_fields(form.vars))

	elif form.errors:
		response.flash = 'Hay un error en un campo'

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
	formPersona = SQLFORM.factory(db.usuario, db.persona)

	if formPersona.process(session=None, formname='Persona', keepvalues=True).accepted:
		"""
		id_usuario=db.usuario.insert(**db.usuario._filter_fields(formPersona.vars))
		formPersona.vars.persona=id_usuario
		
		id_persona=db.persona.insert(**db.persona._filter_fields(formPersona.vars))
		
		db.no_completado.insert(id_persona=id_persona,id_usuario=id_usuario)
		"""
		print formPersona.vars.values()
		redirect(URL("default","registrousrth2",vars=formPersona.vars))

	elif formPersona.errors:
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'

	return dict(formPersona=formPersona)

def registrousrth2():

	usuario=db.usuario._filter_fields(request.vars)
	persona=db.persona._filter_fields(request.vars)
	print persona

	formBombero = SQLFORM.factory(
		Field('carnet', type='integer', unique=True, requires=IS_INT_IN_RANGE(0, error_message='Debe ser positivo')),
		Field('iniciales', type='string', requires=IS_EMPTY_OR(IS_LENGTH(minsize=2,maxsize=4))),
		Field('tipo_sangre', type='string', requires=IS_IN_SET(['A+','A-','B+','B-','AB+','AB-','O+','O-'], error_message='Debe ser alguno de los tipos válidos'))
		)

	if formBombero.process(session=None, formname='Bombero', keepvalues=True).accepted:

		id_usuario=db.usuario.insert(**usuario)		
		id_persona=db.persona.insert(**persona)

		id_bombero=db.bombero.insert(id_usuario=id_usuario, id_persona=id_persona, **db.bombero._filter_fields(formBombero.vars))
		db.auth_user.insert(**usuario)
		redirect(URL("default","registrousrth_final"))

	elif formBombero.errors:
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'

	return dict(formBombero=formBombero)

# Deseable: Que me muestre el nombre del usuario en el mensaje final
def registrousrth_final():
	return dict()

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

@auth.requires_login()
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
								distinct=db.persona.id)

			if len(tabla) == 0:
				error = True
		else:
			error = True
	else:
		tabla = db(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id))

	if error:
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
