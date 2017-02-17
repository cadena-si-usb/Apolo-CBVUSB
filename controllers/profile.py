def buscarth():

	tablaBomberos = db.executesql("SELECT * FROM bombero;")
	print tablaBomberos

	return dict(tabla=tablaBomberos)