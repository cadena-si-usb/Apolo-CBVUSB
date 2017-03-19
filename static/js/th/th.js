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

    // Función para los botones para añadir telefonos
    $("body").on("click","button.agregartlf", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número del usuario al que corresponde el telefono
    var tlfs = "#tlf" + num1;                         // Generar el identificador al contenedor de la unidad correspondiente

    tlfsCont[num1-1]++;                                // Aumentar el contador de telefonos para el usuario
    var num2 = tlfsCont[num1-1];                           // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $("#tlf").append(
            '<div class="form-group" id="tlf'+num2+'">\
                <div class="col-xs-12 col-sm-9 col-sm-offset-3">\
                    <div class="col-xs-12 col-sm-4" style="padding-top: 2%;">\
                        <select name="tipotlf'+num1+'-'+num2+'" class="form-control" data-validation="required">\
                            <option value="">Tipo</option>\
                            <option value="Casa">Casa</option>\
                            <option value="Trabajo">Trabajo</option>\
                            <option value="Otro">Otro</option>\
                        </select>\
                    </div>\
                    <div class="col-xs-12 col-sm-8" style="padding-top: 2%;">\
                        <input type="tel" class="form-control" id="tlf'+num1+'-'+num2+'" name="tlf'+num1+'-'+num2+'" data-validation="length" data-validation-length="12-20" data-validation="number" data-validation-allowing="-+()" placeholder="Teléfono...">\
                    </div>\
                    <div class="text-right" id="quitartlf'+num2+'">\
                        <button id="quitartlf'+num1+'-'+num2+'" type="button" class="btn btn-primary quitartlf top-space-separator"><span>Eliminar Teléfono</span></button>\
                    </div>\
                </div>\
            </div>'
        );
    });

    $("body").on("click","button.quitartlf", function() {
        var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número del usuario al que corresponde el telefono
        var tag_eliminar = "#tlf"+tlfsCont[num1-1];
        $(tag_eliminar).remove();
        tlfsCont[num1-1]--;
    });   

    var dirsCont = [1];

    // Función para los botones para añadir direcciones
    $("body").on("click","button.agregardireccion", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número del usuario al que corresponde el telefono
    var dirs = "#dir" + num1;                         // Generar el identificador al contenedor de la unidad correspondiente

    dirsCont[num1-1]++;                                // Aumentar el contador de telefonos para el usuario
    var num2 = dirsCont[num1-1];                         // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $("#direccion").append(
            '<div class="form-group" id="dir'+num2+'">\
                <div class="col-xs-12 col-sm-9 col-sm-offset-3">\
                    <div class="col-xs-12 col-sm-4" style="padding-top: 2%;">\
                        <select id="direccion_tipo'+num1+'-'+num2+'" name="direccion_tipo'+num1+'-'+num2+'" class="form-control"  data-validation="string" data-validation="required">\
                            <option value="">Tipo</option>\
                            <option value="Casa">Casa</option>\
                            <option value="Trabajo">Trabajo</option>\
                            <option value="Otro">Otro</option>\
                        </select>\
                    </div>\
                    <div class="col-xs-12 col-sm-8" style="padding-top: 2%;">\
                        <input type="dir_c" class="form-control" id="direccion_ciudad'+num1+'-'+num2+'" name="direccion_ciudad'+num1+'-'+num2+'" data-validation="string" data-validation="required" placeholder="Ciudad...">\
                    </div>\
                </div>\
                <div class="col-xs-12 col-sm-9 col-sm-offset-3" style="padding-top: 2%;">\
                    <input type="dir_d" class="form-control" id="direccion_descripcion'+num1+'-'+num2+'" name="direccion_descripcion'+num1+'-'+num2+'" data-validation="string" data-validation="required" placeholder="Descripción...">\
                    <div class="text-right" id="quitardireccion'+num2+'">\
                        <button id="quitardireccion'+num1+'-'+num2+'" type="button" class="btn btn-primary quitardireccion top-space-separator"><span>Eliminar Dirección</span></button>\
                    </div>\
                </div>\
            </div>'
        );
    });

    $("body").on("click","button.quitardireccion", function() {
        var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número del usuario al que corresponde el telefono
        var tag_eliminar = "#dir"+dirsCont[num1-1];
        $(tag_eliminar).remove();
        dirsCont[num1-1]--;
    }); 

    // Funcion para ingresar carnet solo cuando tu cargo no es estudiante
    $("select[name=no_table_cargo]").change(function(){
        var cargo = $('select[name=no_table_cargo]').val();
        if (cargo != "Estudiante") {
            $("#no_table_carnet__row").remove();
            $("#no_table_cargo__row").after(
                '<div id="no_table_carnet__row" class="form-group">\
                    <label if="no_table_carnet__label" class="control-label col-sm-3" for="no_table_carnet">Carnet *</label>\
                    <div class="col-sm-9">\
                        <input id="no_table_carnet" class="form-control string" type="text" name="carnet">\
                    </div>\
                </div>');
        }
        else {
            $("#no_table_carnet__row").remove();
        }
    });
});
