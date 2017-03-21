$(document).ready(function() {
    // Función para configurar los dataTables
    $('.service-table').dataTable( {
        searching: false,
        paginate: false,
        "language": {
            "decimal":        "",
            "infoEmpty":      "",
            "infoPostFix":    "",
            "thousands":      ",",
            "emptyTable":     "No hay servicios para mostrar",
            "lengthMenu":     "Resultados por página: _MENU_",
            "zeroRecords":    "No se han encontrado coincidencias de servicios",
            "info":           "",
            "infoFiltered":   "(Filtrado de _MAX_ registros en total)",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "paginate": {
                "first":    "Primero",
                "last":     "Último",
                "next":     "Siguiente",
                "previous": "Anterior"
            },
            "aria": {
                "sortAscending":  ": Ordenar columna de manera ascendente",
                "sortDescending": ": Ordenar columna de manera descendente"
            }
        }
    });
});
