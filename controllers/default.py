# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
# psql -U cbvusb -h localhost -W

import re
import time
import gluon
import datetime

from gluon.tools import Auth, Service, PluginManager
from gluon.contrib.login_methods.ldap_auth import ldap_auth

def usernotconfirmedsent():
	T.force('es')
	return dict()

def usernotconfirmed():	# HAY QUE VER SI EXISTE EL USUARIO EN CONFIRMACIÓN PARA NOTIFICAR
	T.force('es')
	error = False
	tipo = ""

	default_cedula = ""
	default_genero = ""
	default_carnet = ""
	default_cargo  = ""
	default_rango  = ""
	default_tipo_sangre = ""

	bombero = db(db.bombero.id_usuario==auth.user.id).select()

	if len(bombero) != 0:
		persona = db(db.persona.id==bombero.first().id_persona).select().first()

		default_cedula = persona.cedula
		default_genero = persona.genero
		default_carnet = bombero.first().carnet
		default_cargo  = bombero.first().cargo
		default_rango  = bombero.first().rango
		default_tipo_sangre = bombero.first().tipo_sangre

		redirect(URL('default','usernotconfirmedsent'))

	varsForm = dict((k,v) for k,v in request.vars.iteritems() if v != '')

	if len(request.vars) != len(varsForm):
		error = True

	elif len(request.vars):

		if not(db((db.persona.cedula==request.vars.cedula) & (db.bombero.id_persona==db.persona.id) & (db.bombero.id_usuario != auth.user.id)).isempty()):
			error = True

		if not(db((db.bombero.carnet == request.vars.carnet) & (db.bombero.id_usuario != auth.user.id) & (db.bombero.carnet != 0)).isempty()):
			error = True

		if not error:
			if db(db.bombero.id_usuario==auth.user.id).isempty():
				db(db.usuario.id==auth.user.id).update( first_name=request.vars.primer_nombre, last_name=request.vars.primer_apellido, email=request.vars.email_principal, **db.usuario._filter_fields(request.vars))
				id_persona = db.persona.insert( **db.persona._filter_fields(request.vars))
				db.bombero.insert( id_usuario=auth.user.id, id_persona=id_persona, **db.bombero._filter_fields(request.vars))

			else:
				db(db.usuario.id==auth.user.id).update( first_name=request.vars.primer_nombre, last_name=request.vars.primer_apellido, **db.usuario._filter_fields(request.vars))
				db(db.bombero.id_usuario==auth.user.id).update( **db.persona._filter_fields(request.vars))
				db.bombero.insert( id_usuario=auth.user.id, id_persona=id_persona, **db.bombero._filter_fields(request.vars))

			bombero = db((db.bombero.id_usuario==auth.user.id) & (db.usuario.id==auth.user.id) & (db.persona.id==db.bombero.id_persona)).select().first()

			mail.send(to=[bombero.usuario.email], subject='Confirmación de usuario: Pendiente',
				message='Estimado '+bombero.usuario.username+' su información acaba de ser enviada y pronto le será notificado el resultado.\n\n'+
						'Su información ingresada fue la siguiente:\n\n'+
						'\tCedula: '+str(bombero.persona.cedula)+'\n'+
						'\tNombre: '+bombero.persona.primer_nombre+'\n'+
						'\tApellido: '+bombero.persona.primer_apellido+'\n'+
						'\tGenero: '+bombero.persona.genero+'\n'+
						'\tRango: '+bombero.bombero.rango+'\n'+
						'\tCargo: '+bombero.bombero.cargo+'\n'+
						'\tCarnet: '+str(bombero.bombero.carnet)+'\n\n'+
						'Sistema de Gestión Apolo. CBVUSB.')
			redirect(URL('default','usernotconfirmedsent'))

	if not error:
		tipo="success"
		#response.flash = 'Cambios realizados satisfactoriamente.'
	else:
		tipo="danger"
		response.flash = 'Hay un error en un campo'

	return dict(tipo=tipo)

def userblocked():
	T.force('es')
	return dict()

@auth.requires_permission('Administrador')
def confirmar():
	T.force('es')

	if request.args:
		opcion = request.args[0]
		id_bombero = int(request.args[1])
		bombero = db(db.bombero.id==id_bombero).select().first()

		if opcion == 'editar':
			redirect(URL("default","editarnoconfirmado", args=[id_bombero]))

		if opcion == 'cancelar':
			bombero = db((db.bombero.id==bombero.id) & (db.usuario.id==bombero.id_usuario)).select().first()

			mail.send(to=[bombero.usuario.email], subject='Confirmación de usuario: Rechazada',
			message='Estimado '+bombero.usuario.username+' su solicitud de confirmación acaba de ser Rechaza.\n\n'+
					'Debe ingresar nuevamente al sistema con las credenciales antes enviadas y rellenar la información nuevamente.\n\n'+
					'Cualquier duda con respecto a lo antes mencionado, por favor contacte con el administrador\n\n'+
					'Sistema de Gestión Apolo. CBVUSB.')

			db(db.persona.id==bombero.bombero.id_persona).delete()
			db(db.bombero.id==id_bombero).delete()

		if opcion == 'confirmar':
			actualizar_permisos(bombero.id_usuario, bombero.cargo)
			db(db.usuario.id==bombero.id_usuario).update(confirmed=True)
			
			bombero = db((db.bombero.id_usuario==bombero.id_usuario) & (db.usuario.id==bombero.id_usuario)).select().first()

			mail.send(to=[bombero.usuario.email], subject='Confirmación de usuario: Confirmado',
			message='Estimado '+bombero.usuario.username+' su solicitud de confirmación acaba de ser aprobada y puede acceder al sistema.\n\n'+
					'Le recordamos que sus credenciales fueron enviadas en un correo anterior, para ingresar debe:\n\n'+
					'\t1. Ingresar con las credenciales que le fueron enviadas anteriormente.\n'+
					'\t2. Tras ingresar le recomendamos que vaya a la pestaña '+bombero.usuario.username+' y modifique su contraseña en modificar perfil.\n'+
					'\t3. Le invitamos a completar la información personal en la pestaña de modificar.\n\n'+
					'Sistema de Gestión Apolo. CBVUSB.')

			redirect(URL("default","confirmar"))

		if opcion == 'eliminar':
			if not db(db.bombero.id_usuario==id_bombero).isempty():
				id_persona = db(db.bombero.id_usuario==id_bombero).select().first().id_persona
				db(db.bombero.id_usuario==id_bombero).delete()
				db(db.persona.id==id_persona).delete()

			db(db.usuario.id==id_bombero).delete()

	tabla = db((db.bombero.id_persona==db.persona.id) & (db.usuario.id==db.bombero.id_usuario) & (db.usuario.confirmed == False)).select( distinct=db.bombero.carnet, orderby=~db.bombero.carnet)
	no_confirmados = db((db.usuario.confirmed==False)).select(db.usuario.ALL)

	return dict(tabla=tabla, no_confirmados=no_confirmados)

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

@auth.requires_permission('Administrador')
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
	T.force('es')					
	return dict()

def user():
	T.force('es')
	return dict(form=auth())

@cache.action()
def download():
	return response.download(request, db)

@auth.requires_login()
def call():
	return service()
	
