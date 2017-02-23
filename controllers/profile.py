def buscarth():

	tabla = db.(db.persona).select(join=db.bombero.on(db.bombero.id_persona == db.persona.id))

	return dict(tabla=tablaBomberos)

def registrousr():

	return dict()