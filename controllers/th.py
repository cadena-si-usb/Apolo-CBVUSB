# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
# psql -U cbvusb -h localhost -W

import re
import time
from datetime import *
from gluon.serializers import json

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones que conforman las vistas de Talento Humano
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@auth.requires_login()
def perfilth():

	if request.args:
		userid = int(request.args[0])
	else:
		userid = auth.user.id

	usuario = db(db.bombero.id_usuario==userid).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id)).first()
	
	if usuario is None:
		usuario = db(db.bombero.id_usuario==auth.user.id).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id)).first()

	return dict(usuario=usuario)

@auth.requires_login()
def perfilmodth():
	T.force('es')
	userid = auth.user.id
	bombero=db(db.bombero.id_usuario==userid).select().first()
	persona=db(db.persona.id==bombero.id_persona).select().first()
	usuario=db(db.usuario.id==userid).select().first()
	tipo=""

	# Colocar un campo que diga colocar contraseña actual para cambiar la nueva
	formUsuario = SQLFORM.factory(
		Field('password', 
			type='password', 
			notnull=True,  
			requires=db.usuario.password.requires,
			label='Clave nueva'),
		Field('password_again', 
			type='password', 
			notnull=True, 
			requires=db.usuario.password.requires,
			label='Reingrese la nueva clave'))
	
	if formUsuario.process(session=None, formname='perfilmodUsuario', keepvalues=True).accepted and formUsuario.vars.password==formUsuario.vars.password_again:
		db(db.usuario.id==userid).update(**db.usuario._filter_fields(formUsuario.vars))
		response.flash = 'Cambio de contraseña realizado satisfactoriamente.'
		tipo="success"
	elif formUsuario.process(session=None, formname='perfilmodUsuario', keepvalues=True).accepted:
		tipo="danger"
		response.flash = 'Las contraseñas ingresadas no son iguales'
	elif formUsuario.errors:
		response.flash = 'Hay un error en un campo.'
		tipo="danger"

	formPersona = SQLFORM.factory(
		Field('primer_nombre', 
			type='string', 
			notnull=True, 
			default=persona.primer_nombre, 
			requires=db.persona.primer_nombre.requires,
			label='Primer nombre (*)'
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
			label='Primer apellido (*)'
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
			label='Género (*)'
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
			label='Email principal (*)'
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
			label='Estado civil'
			)
		)

	if formPersona.process(session=None, formname='perfilmodPersona', keepvalues=True).accepted:
		print formPersona.vars['imagen']
		print re.match('^.*\.(jpg|png|jpeg|bmp)$',formPersona.vars['imagen'])
		print
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
		response.flash = 'Cambio realizado satisfactoriamente'
		tipo="success"
	elif formPersona.errors:
		print formPersona.vars
		response.flash = 'Hay un error en un campo'
		tipo="danger"

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
			requires = IS_IN_SET(['Administrador', 
									'Comandante en Jefe', 
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
									'Estudiante'
									], error_message='Debe seleccionar una opción.'),
			label='Cargo que ocupa (*)'),
			Field('rango', 
			type='string', 
			notnull=True,
			default=bombero.rango,
			requires= db.bombero.rango.requires,
			label='Rango (*)'))	#FALTA RANGO
	
	if formBombero.process(session=None, formname='perfilmodBombero', keepvalues=True).accepted:
		db(db.bombero.id_usuario==userid).update(**db.bombero._filter_fields(formBombero.vars))
		user = db(db.bombero.id==userid).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id)).first()
		response.flash = 'Cambio realizado satisfactoriamente.'
		tipo="success"
	elif formBombero.errors:
		response.flash = 'Hay un error en un campo.'
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
				requires=db.usuario.username.requires,
				label='Nombre de usuario (*)'),
		Field('password', 
				type='password', 
				readable=False, 
				length=512, 
				requires=db.usuario.password.requires,
				label='Clave (*)'),
		Field('password_again',
				type='password', 
				readable=False, 
				length=512, 
				requires=db.usuario.password.requires,
				label='Reingrese la clave (*)'),
		Field('nacionalidad', 
				type='string',  
				unique=True, 
				requires=db.persona.nacionalidad.requires,
				label='Nacionalidad (*)'),
		Field('cedula', 
				type='integer',
				length=512, 
				requires=db.persona.cedula.requires,
				label='Cédula (*)'),
		Field('primer_nombre', 
				type='string',
				length=512, 
				requires=db.persona.primer_nombre.requires,
				label='Primer nombre (*)'),
		Field('primer_apellido',
				type='string',
				length=512, 
				requires=db.persona.primer_apellido.requires,
				label='Primer apellido (*)'),
		Field('genero',
				type='string',
				requires=db.persona.genero.requires,
				label='Género (*)'),
		Field('email_principal',
				type='string',
				length=512,
				requires=db.persona.email_principal.requires,
				label='Email principal (*)')
		)

	if formPersona.process(session=None, formname='Persona', keepvalues=True).accepted and formPersona.vars.password==formPersona.vars.password_again:
		formPersona.vars = dict((k,v) for k,v in formPersona.vars.iteritems() if v is not None)
		redirect(URL("th","registrousrth2",vars=formPersona.vars))
	elif formPersona.process(session=None, formname='Persona', keepvalues=True).accepted:
		tipo="danger"
		response.flash = 'Las contraseñas ingresadas no son iguales'
	elif formPersona.errors:
		tipo="danger"
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'

	return dict(formPersona=formPersona,tipo=tipo)

def registrousrth2():
	T.force('es')
	usuario=db.usuario._filter_fields(request.vars)
	persona=db.persona._filter_fields(request.vars)
	tipo=""

	formBombero = SQLFORM.factory(
		Field('carnet', 
				type='integer', 
				unique=True, 
				requires=db.bombero.carnet.requires,
				label='Carnet (*)'),
		Field('cargo', 
			type='string', 
			unique=True, 
			requires = db.bombero.cargo.requires,
			label='Cargo que ocupa (*)'),
		Field('rango', 
			type='string', 
			unique=True,
			requires= db.bombero.rango.requires,
			label='Rango (*)')
		)

	if formBombero.process(session=None, formname='Bombero', keepvalues=True).accepted:

		primer_nombre=persona['primer_nombre']
		primer_apellido=persona['primer_apellido']
		email_principal=persona['email_principal']

		id_usuario=db.usuario.insert(first_name=primer_nombre, last_name=primer_apellido, email=email_principal, **usuario)		
		id_persona=db.persona.insert(**persona)
		id_bombero=db.bombero.insert(id_usuario=id_usuario, id_persona=id_persona, **db.bombero._filter_fields(formBombero.vars))
		redirect(URL("th","registrousrth_final",vars=formBombero.vars,args=id_usuario))

	elif formBombero.errors:
		response.flash = 'Falta un campo por llenar o hay un error en el campo indicado.'
		tipo="danger"

	return dict(formBombero=formBombero,tipo=tipo)

def registrousrth_final():
	T.force('es')
	usuario=db.usuario._filter_fields(request.vars)
	persona=db.persona._filter_fields(request.vars)
	username = str(db.usuario[request.args[0]].username)
	return dict(username=username)

@auth.requires_login()
def eliminarusrth():
	T.force('es')
	userid = auth.user.id

	if len(request.args) > 0:
		
		id_bombero = int(request.args[0])
		
		if not db(db.bombero.id==id_bombero).isempty():
			bombero = db(db.bombero.id==id_bombero).select().first()
			usuario = db(db.usuario.id==bombero.id_usuario).select().first()

			db(db.usuario.id==bombero.id_usuario).update(disable=not(usuario.disable))
			if usuario.disable:
				response.flash = '¡El usuario '+usuario.username+' ha sido habilitado satisfactoriamente!'
			else:
				response.flash = '¡El usuario '+usuario.username+' ha sido deshabilitado satisfactoriamente!'

			tipo = "success"
	tabla = db(db.persona).select(join=db.bombero.on((db.bombero.id_persona == db.persona.id) & 
										(db.bombero.id_usuario!=userid)),
									distinct=db.bombero.carnet,
									orderby=~db.bombero.carnet)
	return dict(tabla=tabla)

@auth.requires_login()
def buscarth():
	T.force('es')
	tabla = db(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id),
										distinct=db.bombero.carnet,
										orderby=~db.bombero.carnet)
	return dict(tabla=tabla)