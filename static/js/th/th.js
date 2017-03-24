$(document).ready(function() {
    var dirsCont = 1; //Contador de las direcciones que se van agregando o quitando
    var tlfsCont = 1; //Contador de los telefonos que se van agregando o quitando
    var max = 5;

    // Función btn hacer clickeables las filas de las tablas y redirigir al href correspondiente
    $(".clickable-row").on('click', function() {
        window.location = $(this).data("href");
    });

    // Tabla para buscar usuarios en talento humano
    $('.buscar-table').dataTable( {
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

    // Botones en tablas, mensajes de alerta antes de ejecutar la accion
    $(function(){
        $('[id="btn-submit-habilitar"]').on('click',function(e){
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
        $('[id="btn-submit-deshabilitar"]').on('click',function(e){
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
        $('[id="btn-submit-eliminar"]').on('click',function(e){
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
        $('[id="btn-submit-confirmar-registro"]').on('click',function(e){
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
        $('[id="btn-submit-cancelar"]').on('click',function(e){
        e.preventDefault();
        var href = $(this).attr('href');
        swal({
            title: "¿Estás seguro de que deseas cancelar la solicitud?",
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
                    title: "Contancia cancelada",
                    type: "success",
                    showConfirmButton: false,
                    html: false
                });
            }
        });
        });
        $('[id="btn-submit-cancelar-registro"]').on('click',function(e){
        e.preventDefault();
        var href = $(this).attr('href');
        swal({
            title: "¿Estás seguro de que deseas cancelar el registro?",
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
                    title: "Registro cancelado",
                    type: "success",
                    showConfirmButton: false,
                    html: false
                });
            }
        });
        });

        $('[id="btn-submit-solicitar"]').on('click',function(e){
        e.preventDefault();
        var href = $(this).attr('href');
        swal({
            title: "¿Estás seguro de que quieres solicitar una constancia?",
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
                    title: "Solicitud enviada",
                    type: "success",
                    showConfirmButton: false,
                    html: false
                });
            }
        });
        });
        $('[id="btn-submit-aprobar"]').on('click',function(e){
        e.preventDefault();
        var href = $(this).attr('href');
        swal({
            title: "¿Estás seguro de que deseas aprobar la constancia?",
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
                    title: "Contancia aprobada",
                    type: "success",
                    showConfirmButton: false,
                    html: false
                });
            }
        });
        });

    });

    // Función para los botones para añadir telefonos
    $("body").on("click","button.agregartlf", function() {
    var tlf = "#tlf"+tlfsCont;
    tlfsCont++;                                // Aumentar el contador de telefonos para el usuario
    var num = tlfsCont;                           // Variable auxiliar para la sustitucion en el html de abajo
    if (num <= max) { 
        // Inserción del html
        $(tlf).after(
                '<div class="form-group" id="tlf'+num+'">\
                    <div class="col-xs-12 col-sm-9 col-sm-offset-3">\
                        <div class="col-xs-12 col-sm-4" style="padding-top: 2%;">\
                            <select id="tipotlf'+num+'" class="form-control" name="telefono'+num+'">\
                                <option value="">Tipo</option>\
                                <option value="Casa">Casa</option>\
                                <option value="Trabajo">Trabajo</option>\
                                <option value="Otro">Otro</option>\
                            </select>\
                        </div>\
                        <div class="col-xs-12 col-sm-8" style="padding-top: 2%;">\
                            <input type="tel" class="form-control" id="tel'+num+'" name="telefono'+num+'" placeholder="Teléfono...">\
                        </div>\
                        <div class="text-right" id="quitartlf'+num+'">\
                            <button id="quitartlf'+num+'" type="button" class="btn btn-primary quitartlf top-space-separator">Eliminar Teléfono <span class="glyphicon glyphicon-remove-sign"></span></button>\
                        </div>\
                    </div>\
                </div>'
            );
        }
    });

    // Funcion para quitar telefono agregado en interfaz
    $("body").on("click","button.quitartlf", function() {
        var tag_eliminar = "#tlf"+tlfsCont;
        $(tag_eliminar).remove();
        tlfsCont--;
    });   

    // Función para los botones para añadir direcciones
    $("body").on("click","button.agregardireccion", function() {
    var dir = "#dir"+dirsCont;
    dirsCont++;                                // Aumentar el contador de telefonos para el usuario
    var num = dirsCont;                         // Variable auxiliar para la sustitucion en el html de abajo
    if (num <= max) {
        // Inserción del html
        $(dir).append(
                '<div class="form-group" id="dir'+num+'">\
                    <div class="col-xs-12 col-sm-9 col-sm-offset-3">\
                        <div class="col-xs-12 col-sm-4" style="padding-top: 2%;">\
                            <select id="direccion_tipo'+num+'" class="form-control" name="direccion'+num+'">\
                                <option value="">Tipo</option>\
                                <option value="Casa">Casa</option>\
                                <option value="Trabajo">Trabajo</option>\
                                <option value="Otro">Otro</option>\
                            </select>\
                        </div>\
                        <div class="col-xs-12 col-sm-8" style="padding-top: 2%;">\
                            <input type="direccion_ciudad'+num+'" class="form-control" id="direccion_ciudad'+num+'" name="direccion'+num+'" placeholder="Ciudad...">\
                        </div>\
                    </div>\
                    <div class="col-xs-12 col-sm-9 col-sm-offset-3" style="padding-top: 2%;">\
                        <input type="direccion_descripcion'+num+'" class="form-control" id="direccion_descripcion'+num+'" name="direccion'+num+'" placeholder="Descripción...">\
                        <div class="text-right" id="quitardireccion'+num+'">\
                            <button id="quitardireccion'+num+'" type="button" class="btn btn-primary quitardireccion top-space-separator">Eliminar Dirección <span class="glyphicon glyphicon-remove-sign"></span></button>\
                        </div>\
                    </div>\
                </div>'
            );
    }
    });

    // Funcion para quitar direccion agregada en interfaz
    $("body").on("click","button.quitardireccion", function() {
        var tag_eliminar = "#dir"+dirsCont;
        $(tag_eliminar).remove();
        dirsCont--;
    }); 

    // Funcion para ingresar carnet solo cuando tu cargo no es estudiante
    $("select[name=cargo]").change(function(){
        var cargo = $('select[name=cargo]').val();

        $('#validadoresGlobales').remove();
        if (cargo != "Estudiante") {
            
            $("#tabla_carnet").remove();
            $("#tabla_cargo").after(
                '<div id="tabla_carnet" class="form-group">\
                    <label class="control-label col-sm-3" for="carnet">Carnet *</label>\
                    <div class="col-sm-9">\
                        <input id="carnet" class="form-control string" type="text" name="carnet">\
                    </div>\
                </div>');
            $('#validador-here').append('<input id="validadoresGlobales"type="hidden" data-validation="cedulaVal, carnetVal, primerApellidoVal, primeroNombreVal">');
        }      
        else {
            $("#tabla_carnet").remove();
            $('#validador-here').append('<input id="validadoresGlobales"type="hidden" data-validation="cedulaVal,  primerApellidoVal, primeroNombreVal">');
        }

    });

    // Placeholders que faltan, especificamente de los SQLFORM de web2py
    $('#no_table_segundo_nombre').attr('placeholder', 'Segundo nombre...');
    $('#no_table_segundo_apellido').attr('placeholder', 'Segundo apellido...');
    $('#no_table_fecha_nacimiento').attr('placeholder', 'dd/mm/año');
    $('#no_table_email_alternativo').attr('placeholder', 'ejemplo@website.com');
    $('#no_table_password_actual').attr('placeholder', 'Clave actual...');
    $('#no_table_password').attr('placeholder', 'Clave nueva...');
    $('#no_table_password_again').attr('placeholder', 'Clave nueva...');
    $('#no_table_email').attr('placeholder', 'ejemplo@website.com');
    $('#no_table_username').attr('placeholder', 'Nombre de usuario...');
    $('#no_table_first_name').attr('placeholder', 'Primer nombre...');
    $('#no_table_last_name').attr('placeholder', 'Primer Apellido');
});
