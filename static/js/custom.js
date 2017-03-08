$(document).ready(function() {
    var comissionsCNT = $("#comissionsCNT"); // ID del contenedor de las comisiones
    var addComission = $("#addComission");   // ID del botón para añadir comisiones
    var comissionsCount = 1;                 // Contador de comisiones
    var unitsCount = [1];                    // Arreglo para contar las unidades (Por defecto 1)
    var comissionMembersCount = [3];         // Arreglo para contar los acompañantes (Por defecto 3)

    // Función para hacer clickeables las filas de las tablas y redirigir al href correspondiente
    $(".clickable-row").on('click', function() {
        window.location = $(this).data("href");
    });

    // Función para los botones para añadir unidades
    $("body").on("click","a.addUnit", function() {
        var num1 = parseInt(this.id.match(/\d+/g), 10 ); // Obtener el número de la comisión a la que corresponde la unidad
        var unitCNT = "#unitsCNT" + num1;                // Generar el identificador al contenedor de la unidad correspondiente

        unitsCount[num1-1]++;                            // Aumentar el contador de unidades para la comisión permitente
        var num2 = unitsCount[num1-1];                   // Variable auxiliar para la sustitucion en el html de abajo

        // Inserción del html
        $(unitCNT).append(
        '<div id="unit'+num1+'-'+num2+'" name="unit'+num1+'-'+num2+'">\
          <div class="col-xs-4 col-sm-2">\
            <select id="unitValue'+num1+'-'+num2+'" class="form-control" name="unitValue'+num1+'-'+num2+'">\
              <option value="" selected="selected">--</option>\
              <option value="1">A1</option>\
              <option value="2">M2</option>\
              <option value="3">L1</option>\
            </select>\
          </div>\
          <div class="col-xs-8 col-sm-10">\
            <input id="comissionDriver'+num1+'-'+num2+'" type="text" class="form-control col-xs-6" placeholder="Conductor" name="comissionDriver'+num1+'-'+num2+'">\
          </div>\
        </div>');
    });

    // Función para los botones para añadir acompañantes
    $("body").on("click","a.addComissionMember", function() {
        var num1 = parseInt(this.id.match(/\d+/g), 10 );         // Obtener el número de la comisión al que corresponde el acompañante
        var comissionMembersCNT = "#comissionMembersCNT" + num1; // Generar el identificador al contenedor del acompañante

        comissionMembersCount[num1-1]++;                         // Aumentar el contador de acompañantes para la comisión permitente
        var num2 = comissionMembersCount[num1-1];                // Variable auxiliar para la sustitucion en el html de abajo

        // Inserción del html
        $(comissionMembersCNT).append('<input type="text" class="form-control" id="comissionMember'+num1+'-'+num2+'" placeholder="Sancho Panza" name="comissionMember'+num1+'-'+num2+'">');
    });

    // Función para el botón para añadir nuevas comisiones
    $(addComission).on('click', function() {
        comissionsCount++;                                          // Aumentar el contador de comisiones
        unitsCount = unitsCount.concat([1]);                        // Agregar un nuevo slot contador de unidades
        comissionMembersCount = comissionMembersCount.concat([3]);  // Agregar un nuevo slot contador de acompañantes

        var num1 = comissionsCount;                                 // Variable auxiliar para la sustitucion en el html de abajo
        var num2 = unitsCount[num1-1];                              // Variable auxiliar para la sustitucion en el html de abajo

        // Inserción del html
        $(comissionsCNT).append(
        '<div id="comission'+num1+'">\
          <div class="row">\
            <div class="col-xs-12">\
              <h3 id="comissionTitle'+num1+'" name="comissionTitle'+num1+'">Comisión <kbd>'+num1+'</kbd></h3>\
              <input type="hidden" name="comissionTitle'+num1+'" value="comissionTitle'+num1+'">\
            </div>\
          </div>\
          <div class="row">\
            <div class="col-xs-12 col-sm-6">\
              <div class="form-group ui-widget">\
                <label for="commissionBoss'+num1+'">Jefe de comisión</label>\
                <input id="commissionBoss'+num1+'" type="text" class="form-control" placeholder="Don Quijote" name="commissionBoss'+num1+'">\
              </div>\
              <label for="unitTitle'+num1+'">Unidades</label>\
              <div class="row">\
                <div id="unitsCNT'+num1+'">\
                  <div id="unit'+num1+'-'+num2+'" name="unit'+num1+'-'+num2+'">\
                    <div class="col-xs-4 col-sm-2">\
                      <select id="unitValue'+num1+'-'+num2+'" class="form-control" name="unitValue'+num1+'-'+num2+'">\
                        <option value="" selected="selected">--</option>\
                        <option value="1">A1</option>\
                        <option value="2">M2</option>\
                        <option value="3">L1</option>\
                      </select>\
                    </div>\
                    <div class="col-xs-8 col-sm-10">\
                      <input id="comissionDriver'+num1+'-'+num2+'" type="text" class="form-control col-xs-6" placeholder="Conductor" name="comissionDriver'+num1+'-'+num2+'">\
                    </div>\
                  </div>\
                </div>\
                <div class="col-xs-12 text-right">\
                  <a href="#" id="addUnit'+num1+'" class="addUnit" role="button">\
                    <small>Añadir unidad <span class="glyphicon glyphicon-wrench"></span></small>\
                  </a>\
                </div>\
              </div>\
            </div>\
            <div class="col-xs-12 col-sm-6">\
              <div id="comissionMembersCNT'+num1+'">\
                <label for="comissionMember'+num1+'-'+num2+'">Acompañantes</label>\
                <input type="text" class="form-control" id="comissionMember'+num1+'-1" placeholder="Sancho Panza" name="comissionMember'+num1+'-1">\
                <input type="text" class="form-control" id="comissionMember'+num1+'-2" placeholder="Sancho Panza" name="comissionMember'+num1+'-2">\
                <input type="text" class="form-control" id="comissionMember'+num1+'-3" placeholder="Sancho Panza" name="comissionMember'+num1+'-3">\
              </div>\
              <div class="text-right">\
                <a href="#" id="addComissionMember'+num1+'" class="addComissionMember" role="button">\
                  <small>Añadir acompañante <span class="glyphicon glyphicon-user"></span></small>\
                </a>\
              </div>\
            </div>\
          </div>\
        </div>');

    });

    // Función para popUp al momento de enviar un servicio
    $('#btn-submit').on('click',function(e){
        e.preventDefault();
        var form = $('#registro');
        swal({
            title: "¿Estás seguro de enviar?",
            text: "Asegúrate de haber llenado todos los campos pertinentes",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#1565C0",
            confirmButtonText: "Si, enviar!",
            cancelButtonText: "Aun no termino",
            closeOnConfirm: false,
            html: false
        }, function(isConfirm) {
                if (isConfirm) { form.submit();
                    swal("Enviado!",
                    "Se ha registrado el servicio satisfatoriamente",
                    "success");
                }
        });
    });
});