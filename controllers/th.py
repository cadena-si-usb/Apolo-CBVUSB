# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
# psql -U cbvusb -h localhost -W

# Limitar la vista de aprobar según la jerarquía

import re
import time
import random
import string
from datetime import *
from gluon.serializers import json

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones auxiliares que conforman las vistas de Talento Humano
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def random_password():
	password = ''
	specials=r'!#$*?'         
	for i in range(0,3):
		password += random.choice(string.lowercase)
		password += random.choice(string.uppercase)
		password += random.choice(string.digits)
		password += random.choice(specials)            
	return ''.join(random.sample(password,len(password)))

def actualizar_permisos( id_usuario, cargo ):

	estudiante 	= '^Estudiante$'
	bombero		= '^Miembro.*$'
	gerencia	= '^.*[Gg]erente.*$'
	inspector	= '^Inspector$'
	comandancia = '^.*[Cc]omandante$'

	if not db(db.auth_membership.user_id==id_usuario).isempty():
		grupo = db(db.auth_membership.user_id==id_usuario).select().first().group_id
		auth.del_membership(grupo, id_usuario)

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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman las vistas de Talento Humano
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@auth.requires_login()
def perfilth():

	if request.args:
		userid = int(request.args[0])
	else:
		userid = auth.user.id

	usuario = db((db.bombero.id_usuario==userid) & (db.bombero.id_persona == db.persona.id)).select().first()
	contacto = db((db.contacto.id_bombero==userid) & (db.bombero.id_persona == db.contacto.id_bombero)).select(db.contacto.ALL).first()
	telefono = db((db.telefono.id_persona==userid) & (db.telefono.id_persona == db.bombero.id_persona)).select(db.telefono.ALL)
	direccion = db((db.bombero.id_usuario==userid) & (db.direccion.id_persona==db.bombero.id_persona)).select(db.direccion.ALL)
		
	if usuario is None:
		usuario = db(db.bombero.id_usuario==auth.user.id).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id)).first()
	
	return dict(usuario=usuario,contacto=contacto,telefono=telefono, direccion=direccion)

@auth.requires_login()
def perfilmodth():
	T.force('es')
	userid = auth.user.id
	bombero=db(db.bombero.id_usuario==userid).select().first()
	persona=db(db.persona.id==bombero.id_persona).select().first()
	usuario=db(db.usuario.id==userid).select().first()
	tipo=""
	error = False

	# Colocar un campo que diga colocar contraseña actual para cambiar la nueva
	formUsuario = SQLFORM.factory(
		Field('password_actual',
			type='password',
			notnull=True,
			requires=db.usuario.password.requires+[IS_EQUAL_TO(usuario.password, error_message='La clave no coincide')],
			label='Ingrese la clave actual'),
		Field('password', 
			type='password', 
			notnull=True,  
			requires=db.usuario.password.requires,
			label='Ingrese la nueva clave'),
		Field('password_again', 
			type='password', 
			notnull=True, 
			requires= db.usuario.password.requires,
			label='Reingrese la nueva clave'))
	if formUsuario.process(session=None, formname='perfilmodUsuario', keepvalues=True).accepted and formUsuario.vars.password==formUsuario.vars.password_again:
		db(db.usuario.id==userid).update(**db.usuario._filter_fields(formUsuario.vars))
		response.flash = 'Cambio de contraseña realizado satisfactoriamente.'
		tipo="success"
	elif formUsuario.process(session=None, formname='perfilmodUsuario', keepvalues=True).accepted:
		tipo="danger"
		response.flash = 'Las contraseñas ingresadas no coinciden'
	elif formUsuario.errors:
		error = True
		tipo="danger"
		response.flash = 'Hay un error en un campo.'

	formPersona = SQLFORM.factory(
		Field('primer_nombre', 
			type='string', 
			notnull=True, 
			default=persona.primer_nombre, 
			requires=db.persona.primer_nombre.requires,
			label='Primer nombre *'
			),
		Field('segundo_nombre', 
			type='string',
			default=persona.segundo_nombre, 
			requires=db.persona.segundo_nombre.requires,
			label='Segundo nombre'
			),
		Field('primer_apellido', 
			type='string', 
			notnull=True, 
			default=persona.primer_apellido, 
			requires=db.persona.primer_apellido.requires,
			label='Primer apellido *'
			),
		Field('segundo_apellido', 
			type='string',
			default=persona.segundo_apellido, 
			requires=db.persona.segundo_apellido.requires,
			label='Segundo apellido'
			),
		Field('fecha_nacimiento', 
			type='date', 
			notnull=True,
			#default=date(db.persona.fecha_nacimiento.year, db.persona.fecha_nacimiento.month, db.persona.fecha_nacimiento.day),
			requires=db.persona.fecha_nacimiento.requires,
			label='Fecha de nacimiento'
			),
		Field('lugar_nacimiento', 
			type='string', 
			notnull=True,
			default=persona.lugar_nacimiento, 
			requires=db.persona.lugar_nacimiento.requires,
			label='Estado de nacimiento'
			),
		Field('genero', 
			type='string', 
			notnull=True,
			default=persona.genero, 
			requires=db.persona.genero.requires,
			label='Género *'
			),
		Field('imagen', 
			type='upload',
			uploadfolder=os.path.join(request.folder,'static/profile-images'),
			#default=os.path.join(request.folder,'static/profile-images',persona.imagen)
			requires=db.persona.imagen.requires
			),
		Field('email_principal', 
			type='string', 
			notnull=True,
			default=persona.email_principal, 
			requires=db.persona.email_principal.requires,
			label='Email principal *'
			),
		Field('email_alternativo', 
			type='string',
			default=persona.email_alternativo, 
			requires=db.persona.email_alternativo.requires,
			label='Email secundario'
			),
		Field('estado_civil', 
			type='string', 
			notnull=True,
			default=persona.estado_civil, 
			requires=db.persona.estado_civil.requires,
			label='Estado civil')
		)

	if formPersona.process(session=None, formname='perfilmodPersona', keepvalues=True).accepted:

		if formPersona.vars['fecha_nacimiento'] == None or formPersona.vars['fecha_nacimiento'] == "":
			del formPersona.vars['fecha_nacimiento']        

		if formPersona.vars['imagen'] == None or formPersona.vars['imagen'] == "":
			del formPersona.vars['imagen']

		elif re.match('^.*\.(jpg|png|jpeg|bmp)$',formPersona.vars['imagen']) == None:
			os.remove(os.path.join(request.folder,'static/profile-images',formPersona.vars['imagen']))
			del formPersona.vars['imagen']

		elif persona.imagen != db.persona.imagen.default:
			os.remove(os.path.join(request.folder,'static/profile-images',persona.imagen))

		db(db.persona.id==bombero.id_persona).update(**db.persona._filter_fields(formPersona.vars))

		tipo="success"
		response.flash = 'Cambio realizado satisfactoriamente'
		
	elif formPersona.errors:
		error = True
		tipo="danger"
		response.flash = 'Hay un error en un campo'
		

	formBombero = SQLFORM.factory(
		Field('tipo_sangre', 
			type='string', 
			notnull=True, 
			default=bombero.tipo_sangre,
			requires = db.bombero.tipo_sangre.requires,
			label='Tipo de sangre'),
		Field('iniciales', 
			type='iniciales', 
			notnull=True, 
			default=bombero.iniciales,
			requires=db.bombero.iniciales.requires,
			label='Iniciales'),
		Field('cargo', 
			type='string', 
			notnull=True, 
			default=bombero.cargo,
			requires = IS_IN_SET([	'Comandante en Jefe', 
									'Primer comandante', 
									'Segundo comandante', 
									'Inspector en Jefe', 
									'Gerente de Riesgo', 
									'Gerente de Administración', 
									'Gerente de Educación', 
									'Gerente de Operaciones',
									'Gerente de Talento humano',
									'Sub-Gerente de Riesgo', 
									'Sub-Gerente de Administración', 
									'Sub-Gerente de Educación', 
									'Sub-Gerente de Operaciones',
									'Sub-Gerente de Talento humano',
									'Miembro de Riesgo', 
									'Miembro de Administración', 
									'Miembro de Educación', 
									'Miembro de Operaciones',
									'Miembro de Talento humano',
									'Miembro de Comandancia'
									'Estudiante'
									], error_message='Debe seleccionar una opción.'),
			label='Cargo que ocupa *'),
		Field('rango', 
			type='string', 
			notnull=True,
			default=bombero.rango,
			requires= db.bombero.rango.requires,
			label='Rango *')) #FALTA RANGO
	
	if formBombero.process(session=None, formname='perfilmodBombero', keepvalues=True).accepted:
		actualizar_permisos(userid, formBombero.vars.cargo)
		db(db.bombero.id_usuario==userid).update(**db.bombero._filter_fields(formBombero.vars))
		user = db(db.bombero.id==userid).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id)).first()
		
		tipo="success"
		response.flash = 'Cambio realizado satisfactoriamente.'
		
	elif formBombero.errors:
		error = True
		tipo="danger"
		response.flash = 'Hay un error en un campo.'

	varsForm = dict((k,v) for k,v in request.vars.iteritems() if v != '') 	# Limpieza de vacios

	if len(request.vars):		
		cargo = '^.*cargo$'
		tipo_sangre = '^tipo_sangre$'
		rango = '^rango$'
		telefonos = '^telefono[\d]+$'
		contacto = '^persona_contacto$'
		direccion = '^direccion[\d]+$'

		print request.vars

		for campo in request.vars:

			if re.match(cargo,campo):
				actualizar_permisos( userid, request.vars[campo])
				db(db.bombero.id_usuario==userid).validate_and_update(cargo=request.vars[campo])

			if re.match(tipo_sangre,campo):
				db(db.bombero.id_usuario==userid).validate_and_update(tipo_sangre=request.vars[campo])

			if re.match(rango,campo):
				db(db.bombero.id_usuario==userid).validate_and_update(rango=request.vars[campo])

			if re.match(telefonos,campo):

				tipo_telefono = request.vars[campo][0]
				codigo_telefono = request.vars[campo][1][:4]
				numero_telefono = request.vars[campo][1][4:]

				if codigo_telefono == '' and tipo_telefono == '':
					pass

				elif len(request.vars[campo][1]) != 11 or tipo_telefono == '':
					error = True
					tipo = "danger"
					response.flash = "No puede ingresar datos incompletos"
					print "Error"

				elif db((db.bombero.id_usuario==userid) & (db.bombero.id_persona==db.telefono.id_persona)\
					& (db.telefono.codigo_telefono==codigo_telefono) & (db.telefono.numero_telefono==numero_telefono))\
					.isempty():

					db.telefono.validate_and_insert(id_persona=persona.id, tipo_telefono=tipo_telefono,
													codigo_telefono=codigo_telefono, numero_telefono=numero_telefono)

			if re.match(contacto,campo):
				nombre = request.vars[campo][0]
				tipo_telefono1 = request.vars[campo][1]
				codigo_telefono1 = request.vars[campo][2][:4]
				numero_telefono1 = request.vars[campo][2][4:]
				tipo_telefono2 = request.vars[campo][3]
				codigo_telefono2 = request.vars[campo][4][:4]
				numero_telefono2 = request.vars[campo][4][4:]

				if nombre=='' and tipo_telefono1=='' and codigo_telefono1=='' and numero_telefono1==''\
					and tipo_telefono2=='' and codigo_telefono2 == '' and numero_telefono2 == '':
					pass

				elif len(request.vars[campo][2]) != 11 or tipo_telefono1 == ''\
						or len(request.vars[campo][4]) != 11 or tipo_telefono2 == '' or nombre=='':
					error = True
					tipo = "danger"
					response.flash = "No puede ingresar datos incompletos"
					print "Error"

				elif db((db.bombero.id_usuario==userid) & (db.contacto.id_bombero==bombero.id)).isempty():
					db.contacto.insert(id_bombero=bombero.id, nombre=nombre, 
							tipo_telefono1=tipo_telefono1, codigo_telefono1=codigo_telefono1, numero_telefono1=numero_telefono1,
							tipo_telefono2=tipo_telefono2, codigo_telefono2=codigo_telefono2, numero_telefono2=numero_telefono2)

				elif not db((db.bombero.id_usuario==userid) & (db.contacto.id_bombero==bombero.id)).isempty():
					db(db.contacto.id_bombero==bombero.id).update(nombre=nombre, 
							tipo_telefono1=tipo_telefono1, codigo_telefono1=codigo_telefono1, numero_telefono1=numero_telefono1,
							tipo_telefono2=tipo_telefono2, codigo_telefono2=codigo_telefono2, numero_telefono2=numero_telefono2)

			if re.match(direccion,campo):
				direccion_tipo = request.vars[campo][0]
				direccion_ciudad = request.vars[campo][1]
				direccion_descripcion = request.vars[campo][2]

				if direccion_tipo == '' and direccion_ciudad == '' and direccion_descripcion == '':
					pass

				elif direccion_tipo == '' or direccion_ciudad == '' or direccion_descripcion == '':
					error = True
					tipo = "danger"
					response.flash = "No puede ingresar datos incompletos"
					print "Error"

				else:
					db.direccion.insert(id_persona=persona.id, direccion_tipo=direccion_tipo,
										direccion_ciudad=direccion_ciudad, direccion_descripcion=direccion_descripcion)

		if not error:
			tipo="success"
			response.flash = 'Cambios realizados satisfactoriamente.'
		else:
			tipo="danger"
			response.flash = 'Hay un error en un campo'

	return dict(formBombero=formBombero,formPersona=formPersona,formUsuario=formUsuario,tipo=tipo)  

# DEBO CONSIDERAR EL NONE! Si es None colocar entonces ''
@auth.requires_permission('Gerencia')
def registrousrth():
	T.force('es')
	tipo=""
	formUsuario = SQLFORM.factory(
		Field('username', 
			type='string', 
			length=512, 
			unique=True, 
			requires=db.usuario.username.requires,
			label='Nombre de usuario *'),
		Field('first_name', 
			type='string',
			length=512, 
			requires=db.persona.primer_nombre.requires,
			label='Primer nombre *'),
		Field('last_name',
			type='string',
			length=512, 
			requires=db.persona.primer_apellido.requires,
			label='Primer apellido *'),
		Field('email',
			type='string',
			length=512,
			requires=db.usuario.email,
			label='Email principal *')
		)

	if formUsuario.process(session=None, formname='Persona', keepvalues=True).accepted:
		password = random_password()
		if mail.send(to=[formUsuario.vars.email], subject='Creación de usuario',
			message='Acaba de ser creado un usuario para usted en el sistema Apolo. El usuario posee las siguientes credenciales:\n\n'+
					'username: '+formUsuario.vars.username+'\n'
					'password: '+password+'\n\n'+
					'Para completar el registro debe llenar sus datos básicos y esperar la confirmación de parte del administrador.\n'+
					'Bienvenido a Apolo. CBVUSB.'):
			password =  CRYPT()(password)[0]
			id_usuario = db.usuario.insert( password=password, **db.usuario._filter_fields(formUsuario.vars))
			redirect(URL("th","registrousrth_final",args=id_usuario))
		else:
			tipo="danger"
			response.flash = 'El correo no pudo ser entregado a su destinatario, confirmar la validez del mismo.'
	
	elif formUsuario.process(session=None, formname='Persona', keepvalues=True).accepted:
		tipo="danger"
		response.flash = 'Las contraseñas ingresadas no son iguales'
	
	elif formUsuario.errors:
		tipo="danger"
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'

	return dict(formUsuario=formUsuario,tipo=tipo)

def registrousrth_final():
	T.force('es')
	username = str(db(db.usuario.id==request.args[0]).select().first().username)
	return dict(username=username)

@auth.requires_login()
def deshabilitarth():
	T.force('es')
	userid = auth.user.id

	if len(request.args) > 0:
		
		id_bombero = int(request.args[0])
		
		if not db(db.bombero.id==id_bombero).isempty():
			bombero = db(db.bombero.id==id_bombero).select().first()
			usuario = db((db.usuario.id==bombero.id_usuario)).select().first()

			db(db.usuario.id==bombero.id_usuario).update(disable=not(usuario.disable))

			#tipo = "success"
			#if usuario.disable:
			#	response.flash = '¡El usuario '+usuario.username+' ha sido habilitado satisfactoriamente!'
			#else:
			#	response.flash = '¡El usuario '+usuario.username+' ha sido deshabilitado satisfactoriamente!'

	tabla = db((db.persona.id==db.bombero.id_persona) & (db.usuario.id==db.bombero.id_usuario)\
				& (db.bombero.id_usuario!=userid) & (db.usuario.confirmed==True) & (db.bombero.carnet!="-1"))\
				.select(distinct=db.bombero.carnet,	orderby=~db.bombero.carnet)

	return dict(tabla=tabla)

@auth.requires_permission('Estudiante')
def buscarth():
	T.force('es')
	tabla = db((db.persona.id==db.bombero.id_persona) & (db.usuario.id==db.bombero.id_usuario)\
				& (db.usuario.confirmed==True) & (db.usuario.disable==False) & (db.bombero.carnet!="-1"))\
				.select(distinct=db.bombero.carnet,	orderby=~db.bombero.carnet)

	return dict(tabla=tabla)

@auth.requires_login()
def constancia():
	T.force('es')
	return dict()

@auth.requires_login()
def gestionarconstancia():
	T.force('es')
	tipo = ""
	no_solicitado = db(db.constancia.id_solicitante==auth.user.id).isempty()

	usuario = db((db.bombero.id_usuario==auth.user.id) & (db.persona.id==db.bombero.id_persona)).select().first()

	if request.args:
		solicitud = request.args[0]

		if solicitud == 'solicitar':
			if not no_solicitado:
				tipo = "danger"
				response.flash = "Ya tiene una solicitud pendiente."
				
			else:
				db.constancia.insert(id_solicitante=auth.user.id)

		if solicitud == 'aprobar' and len(request.args) > 1:
			db(db.constancia.id == request.args[1]).delete()
			mail.send(to=[bombero.usuario.email], 
						subject='Solicitud de constancia: Aprobada',
						message='Estimado '+bombero.usuario.username+' su solicitud de constancia ha sido aprobada por Talento Humano.\n\n'+
								'Adjunto se envía el archivo:\n\n'+
								'Sistema de Gestión Apolo. CBVUSB.')

	tabla = db((db.persona.id==db.bombero.id_persona) & (db.usuario.id==db.bombero.id_usuario)\
				& (db.constancia.id_solicitante==db.usuario.id) & (db.usuario.id!=auth.user.id) & (db.usuario.id!="-1"))\
				.select(distinct=db.bombero.carnet,	orderby=~db.bombero.carnet)

	return dict( usuario=usuario, tabla=tabla, tipo=tipo, no_solicitado=no_solicitado)

"""
mail.send(to=[bombero.usuario.email], subject='Solicitud de constancia: Cancelada',
			message='Estimado '+bombero.usuario.username+' su solicitud de constancia ha sido rechazada por Talento Humano. Sentimos las molestias ocasionadas.\n\n'+
					'Sistema de Gestión Apolo. CBVUSB.')
		redirect(URL('default','usernotconfirmedsent'))
"""