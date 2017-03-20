# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
# psql -U cbvusb -h localhost -W

import re
import time
import gluon
import datetime

from gluon.tools import Auth, Service, PluginManager
from gluon.contrib.login_methods.ldap_auth import ldap_auth
#import gluon.validators

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
def usernotconfirmed():	# HAY QUE VER SI EXISTE EL USUARIO EN CONFIRMACIÓN PARA NOTIFICAR
	T.force('es')
	tipo = ""

	default_cedula = ""
	default_genero = ""
	default_carnet = ""
	default_cargo  = ""
	default_rango  = ""

	bombero = db(db.bombero.id_usuario==auth.user.id).select()

	if len(bombero) != 0:
		persona = db(db.persona.id==bombero.first().id_persona).select().first()

		default_cedula = persona.cedula
		default_genero = persona.genero
		default_carnet = bombero.first().carnet
		default_cargo  = bombero.first().cargo
		default_rango  = bombero.first().rango

	formConfirmar = SQLFORM.factory(
		Field('password', 
			type='password', 
			readable=False, 
			length=512, 
			requires=db.usuario.password.requires,
			label='Clave'
			),
		Field('password_again',
			type='password', 
			readable=False, 
			length=512,
			requires=db.usuario.password.requires,
			label='Reingrese la clave'
			),
		Field('cedula', 
			type='integer',
			length=512,
			default=default_cedula,
			requires=db.persona.cedula.requires,
			label='Cédula'
			),
		Field('primer_nombre', 
			type='string', 
			notnull=True, 
			default=auth.user.first_name, 
			requires=db.persona.primer_nombre.requires,
			label='Primer nombre'
			),
		Field('primer_apellido', 
			type='string', 
			notnull=True, 
			default=auth.user.last_name, 
			requires=db.persona.primer_apellido.requires,
			label='Primer apellido'
			),
		Field('genero', 
			type='string', 
			notnull=True,
			default=default_genero,
			requires=db.persona.genero.requires,
			label='Género'
			),
		Field('email_principal', 
			type='string', 
			notnull=True,
			default=auth.user.email, 
			requires=db.persona.email_principal.requires,
			label='Email principal'
			),
		Field('rango', 
			type='string', 
			notnull=True,
			default=default_rango, 
			requires=db.bombero.rango.requires,
			label='Rango'
			),
		Field('cargo', 
			type='string', 
			notnull=True,
			default=default_cargo, 
			requires=db.bombero.cargo.requires,
			label='Cargo'
			),
		Field('carnet', 
			type='integer', 
			unique=True, 
			default=default_carnet,
			requires=db.bombero.carnet.requires,
			label='Carnet'
			)
		)

	if formConfirmar.process(session=None, formname='confirmar', keepvalues=True).accepted:
		if formConfirmar.vars.password==formConfirmar.vars.password_again:
			if len(bombero) == 0:
				db(db.usuario.id==auth.user.id).update( first_name=formConfirmar.vars.primer_nombre, last_name=formConfirmar.vars.primer_apellido, **db.usuario._filter_fields(formConfirmar.vars))
				id_persona = db.persona.insert( **db.persona._filter_fields(formConfirmar.vars))
				db.bombero.insert( id_usuario=auth.user.id, id_persona=id_persona, **db.bombero._filter_fields(formConfirmar.vars))
			
			else:
				db(db.usuario.id==auth.user.id).update( first_name=formConfirmar.vars.primer_nombre, last_name=formConfirmar.vars.primer_apellido, **db.usuario._filter_fields(formConfirmar.vars))
				db(db.bombero.id_usuario==auth.user.id).update( **db.persona._filter_fields(formConfirmar.vars))
				db.bombero.insert( id_usuario=auth.user.id, id_persona=id_persona, **db.bombero._filter_fields(formConfirmar.vars))

			tipo="success"
			response.flash = 'La solicitud de confirmación fue enviada exitosamente, le será notificado el resultado'
		else:
			tipo="danger"
			response.flash = 'Las contraseñas ingresadas no son iguales'

	elif formConfirmar.errors:
		tipo="danger"
		response.flash = 'Todos los campos deben ser llenados'

	return dict(form=formConfirmar, tipo=tipo)

def userblocked():
	T.force('es')
	return dict()

@auth.requires_permission('Gerencia')
def confirmar():
	T.force('es')

	if request.args:
		opcion = request.args[0]
		id_bombero = int(request.args[1])
		bombero = db(db.bombero.id==id_bombero).select().first()

		if opcion == 'editar':
			redirect(URL("default","editarnoconfirmado", args=[id_bombero]))

		if opcion == 'eliminar':
			db(db.persona.id == bombero.id_persona).delete()
			db(db.bombero.id==id_bombero).delete()

		if opcion == 'confirmar':
			actualizar_permisos(bombero.id_usuario, bombero.cargo)
			db(db.usuario.id==bombero.id_usuario).update(confirmed=True)

	tabla = db((db.bombero.id_persona==db.persona.id) & (db.usuario.id==db.bombero.id_usuario) & (db.usuario.confirmed == False)).select( distinct=db.bombero.carnet, orderby=~db.bombero.carnet)

	#print tabla

	return dict(tabla=tabla)

def actualizar_permisos( id_usuario, cargo ):

	estudiante 	= '^Estudiante$'
	bombero		= '^Miembro.*$'
	gerencia	= '^.*[Gg]erente.*$'
	inspector	= '^Inspector$'
	comandancia = '^.*[Cc]omandante$'

	if re.match(estudiante, cargo):
		auth.add_membership(auth.id_group('Estudiante'), id_usuario)
	elif re.match(bombero, cargo):
		auth.add_membership(auth.id_group('Bombero'), id_usuario)
	elif re.match(gerencia, cargo):
		auth.add_membership(auth.id_group('Gerencia'), id_usuario)
	elif re.match(inspector, cargo):
		auth.add_membership(auth.id_group('Inspectoria'), id_usuario)
	elif re.match(comandancia, cargo):
		auth.add_membership(auth.id_group('Comandancia'), id_usuario)

@auth.requires_permission('Gerencia')
def editarnoconfirmado():
	T.force('es')
	tipo = ""
	
	id_bombero = int(request.args[0])
	bombero = db(db.bombero.id==id_bombero).select().first()

	persona = db(db.persona.id==bombero.id_persona).select().first()
	usuario = db(db.usuario.id==bombero.id_usuario).select().first()

	formEditar = SQLFORM.factory(
		Field('cedula', 
			type='integer',
			length=512, 
			default=persona.cedula,
			requires=IS_INT_IN_RANGE(minimum=1,maximum=100000000, error_message='Número de cedula no valido.'),
			label='Cédula'
			),
		Field('primer_nombre', 
			type='string', 
			notnull=True, 
			default=usuario.first_name, 
			requires=db.persona.primer_nombre.requires,
			label='Primer nombre'
			),
		Field('primer_apellido', 
			type='string', 
			notnull=True, 
			default=usuario.last_name, 
			requires=db.persona.primer_apellido.requires,
			label='Primer apellido'
			),
		Field('genero', 
			type='string', 
			notnull=True,
			default=persona.genero,
			requires=db.persona.genero.requires,
			label='Género'
			),
		Field('rango', 
			type='string', 
			notnull=True,
			default=bombero.rango, 
			requires=db.bombero.rango.requires,
			label='Rango'
			),
		Field('cargo', 
			type='string', 
			notnull=True,
			default=bombero.cargo, 
			requires=db.bombero.cargo.requires,
			label='Cargo'
			),
		Field('carnet', 
			type='integer', 
			unique=True, 
			default=bombero.carnet,
			requires=IS_INT_IN_RANGE(1, error_message='Debe ser positivo'),
			label='Carnet'
			)
		)
		
	if formEditar.process(session=None, formname='editar', keepvalues=True).accepted:
		
		db(db.usuario.id==usuario.id).update( first_name=formEditar.vars.primer_nombre, last_name=formEditar.vars.primer_apellido, **db.usuario._filter_fields(formEditar.vars))
		db(db.persona.id==persona.id).update( **db.persona._filter_fields(formEditar.vars))
		db(db.bombero.id==bombero.id).update( **db.bombero._filter_fields(formEditar.vars))
		
		redirect(URL("default","confirmar"))

	elif formEditar.errors:
		tipo="danger"
		response.flash = 'Todos los campos deben ser llenados'

	return dict(form=formEditar, tipo=tipo)

def index():
	"""
	example action using the internationalization operator T and flash
	rendered by views/default/index.html or views/generic.html

	if you need a simple wiki simply replace the two lines below with:
	return auth.wiki()
	"""
	T.force('es')					
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
