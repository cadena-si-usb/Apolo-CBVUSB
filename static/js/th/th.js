$(document).ready(function() {
    // Función para hacer clickeables las filas de las tablas y redirigir al href correspondiente
    $(".clickable-row").on('click', function() {
        window.location = $(this).data("href");
    });
    // Tabla para buscar usuarios en talento humano
    $('.buscarth-table').dataTable( {
        searching: true,
        "language": {
            "decimal":        "",
            "infoEmpty":      "",
            "infoPostFix":    "",
            "thousands":      ",",
            "emptyTable":     "No hay registros para esta búsqueda.",
            "lengthMenu":     "Resultados por página: _MENU_",
            "zeroRecords":    "No hay registros para esta búsqueda.",
            "info":           "Página _PAGE_ de _PAGES_",
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
    $('.eliminarth-table').dataTable( {
        searching: true,
        "language": {
            "decimal":        "",
            "infoEmpty":      "",
            "infoPostFix":    "",
            "thousands":      ",",
            "emptyTable":     "No hay registros para esta búsqueda.",
            "lengthMenu":     "Resultados por página: _MENU_",
            "zeroRecords":    "No hay registros para esta búsqueda.",
            "info":           "Página _PAGE_ de _PAGES_",
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
    $('.confirmar-table').dataTable( {
        searching: true,
        "language": {
            "decimal":        "",
            "infoEmpty":      "",
            "infoPostFix":    "",
            "thousands":      ",",
            "emptyTable":     "No hay registros para esta búsqueda.",
            "lengthMenu":     "Resultados por página: _MENU_",
            "zeroRecords":    "No hay registros para esta búsqueda.",
            "info":           "Página _PAGE_ de _PAGES_",
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
