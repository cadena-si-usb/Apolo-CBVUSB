$(document).ready(function() {
    // Función para hacer clickeables las filas de las tablas y redirigir al href correspondiente
    $(".clickable-row").on('click', function() {
        window.location = $(this).data("href");
    });

    // Tabla para buscar usuarios en talento humano
    $('.buscarth-table').dataTable( {
        searching: true,
        "language": {
            caseInsen: false,
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
            "searchPlaceholder": "Buscar...",
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
            caseInsen: false,
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
            "searchPlaceholder": "Buscar...",
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

    // Mensaje pop-Up para habilitar un usuario
    $('#btn-submit-habilitar').on('click',function(e){
    e.preventDefault();
    var href = $(this).attr('href');
    swal({
        title: "¿Estás seguro de que quieres habilitar a este usuario?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565C0",
        confirmButtonText: "Si",
        cancelButtonText: "No",
        closeOnConfirm: false,
        html: false
    }, function(isConfirm) {
        if (isConfirm) {
            window.location.href = href;
            swal({
                title: "Usuario habilitado",
                type: "success",
                showConfirmButton: false,
                html: false
            });
        }
    });
    });

    // Mensaje pop-Up para deshabilitar un usuario
    $('#btn-submit-deshabilitar').on('click',function(e){
    e.preventDefault();
    var href = $(this).attr('href');
    swal({
        title: "¿Estás seguro de que quieres deshabilitar a este usuario?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565C0",
        confirmButtonText: "Si",
        cancelButtonText: "No",
        closeOnConfirm: false,
        html: false
    }, function(isConfirm) {
        if (isConfirm) {
            window.location.href = href;
            swal({
                title: "Usuario deshabilitado",
                type: "success",
                showConfirmButton: false,
                html: false
            });
        }
    });
    });

    // Mensaje pop-Up para eliminar el registro de un usuario
    $('#btn-submit-eliminar').on('click',function(e){
    e.preventDefault();
    var href = $(this).attr('href');
    swal({
        title: "¿Estás seguro de que quieres eliminar el registro de este usuario?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565C0",
        confirmButtonText: "Si",
        cancelButtonText: "No",
        closeOnConfirm: false,
        html: false
    }, function(isConfirm) {
        if (isConfirm) {
            window.location.href = href;
            swal({
                title: "Registro eliminado",
                type: "success",
                showConfirmButton: false,
                html: false
            });
        }
    });
    });

    // Mensaje pop-Up para confirmar el registro de  un usuario
    $('#btn-submit-confirmar').on('click',function(e){
    e.preventDefault();
    var href = $(this).attr('href');
    swal({
        title: "¿Estás seguro de que quieres confirmar el registro de este usuario?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565C0",
        confirmButtonText: "Si",
        cancelButtonText: "No",
        closeOnConfirm: false,
        html: false
    }, function(isConfirm) {
        if (isConfirm) {
            window.location.href = href;
            swal({
                title: "Registro confirmado",
                type: "success",
                showConfirmButton: false,
                html: false
            });
        }
    });
    });

    var tlfsCont = [1];

    // Función para los botones para añadir phones
    $("body").on("click","button.agregartlf", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número del usuario al que corresponde el telefono
    var tlfs = "#tlf" + num1;                         // Generar el identificador al contenedor de la unidad correspondiente

    tlfsCont[num1-1]++;                                // Aumentar el contador de telefonos para el usuario
    var num2 = tlfsCont[num1-1];                           // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(tlfs).append(
        '<div class="col-xs-12 col-sm-9 col-sm-offset-3">\
            <div class="col-xs-12 col-sm-4">\
                <select name="codtlf'+num1+'-'+num2+'" class="form-control" data-validation="required">\
                    <option value="">Seleccionar</option>\
                    <option value="0212">0212</option>\
                    <option value="0412">0412</option>\
                    <option value="0414">0414</option>\
                    <option value="0416">0416</option>\
                    <option value="0424">0424</option>\
                    <option value="0426">0426</option>\
                </select>\
            </div>\
            <div class="col-xs-12 col-sm-8">\
                <input type="tel" class="form-control" id="tlf'+num1+'-'+num2+'" name="tlf'+num1+'-'+num2+'" data-validation="length" data-validation-length="12-20" data-validation="number" data-validation-allowing="-+()">\
            </div>\
        </div>'
        );
    });
});
