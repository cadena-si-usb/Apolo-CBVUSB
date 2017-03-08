$(document).ready(function() {
    var comissionsCNT = $("#comissionsCNT"); // ID del contenedor de las comisiones
    var addComission = $("#addComission");   // ID del botón para añadir comisiones
    var comissionsCount = 1;                 // Contador de comisiones
    var unitsCount = [1];                    // Arreglo para contar las unidades (Por defecto 1)
    var comissionMembersCount = [3];         // Arreglo para contar los acompañantes (Por defecto 3)


    var afectadosCNT = $("#afectadosCNT");  // ID del contenedor de los afectados
    var addAfectado = $("#addAfectado");    // ID del botón para añadir Afectados
    var afectadosCount = 1;                 // Contador de afectados
    var emailsCount = [1];                  // Arreglo para contar los emails (Por defecto 1)
    var phoneCount = [1];                   // Arreglo para contar los telefonos (Por defecto 1)


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

    // Función para los botones para añadir emails
    $("body").on("click","a.addEmail", function() {
      var num1 = parseInt(this.id.match(/\d+/g), 10 );  // Obtener el número del afectado al que corresponde el email
      var emailCNT = "#emailCNT" + num1;                // Generar el identificador al contenedor de la unidad correspondiente

      emailsCount[num1-1]++;                             // Aumentar el contador de emails para el afectado permitente
      var num2 = emailsCount[num1-1];                    // Variable auxiliar para la sustitucion en el html de abajo

      // Inserción del html
      $(emailCNT).append('<input type="email" class="form-control" id="phoneMember'+num1+'-'+num2+'" placeholder="josebombero@gmail.com" name="phoneMember'+num1+'-'+num2+'">');
    });


    // Función para los botones para añadir emails
    $("body").on("click","a.addPhone", function() {
      var num1 = parseInt(this.id.match(/\d+/g), 10 );  // Obtener el número del afectado al que corresponde el phone
      var phoneCNT = "#phoneCNT" + num1;                // Generar el identificador al contenedor de la unidad correspondiente

      phoneCount[num1-1]++;                             // Aumentar el contador de phones para el afectado permitente
      var num2 = phoneCount[num1-1];                    // Variable auxiliar para la sustitucion en el html de abajo

      // Inserción del html
      $(phoneCNT).append('<input type="tel" class="form-control" id="phoneMember'+num1+'-'+num2+'" placeholder="0424-8412323" name="phoneMember'+num1+'-'+num2+'">');
    });


    // Función para el botón para añadir afectados adicionales
    $(addAfectado).on('click', function() {
      afectadosCount++;                                           // Aumentar el contador de afectados
      emailsCount = emailsCount.concat([1]);                      // Agregar un nuevo slot contador de emails
      phoneCount = phoneCount.concat([1]);                        // Agregar un nuevo slot contador de phones

      var num1 = afectadosCount;                                 // Variable auxiliar para la sustitucion en el html de abajo
      var num2 = emailsCount[num1-1];                            // Variable auxiliar para la sustitucion en el html de abajo

      // Inserción del html
      $(afectadosCNT).append(
        '<div id="afectado1'+num1+'">\
        <div class="row">\
          <div class="col-xs-6">\
            <h3 class="AfectadoTitle'+num1+'">Afectado #'+num1+'</h3>\
          </div>\
        </div>\
        <div class="row">\
          <div class="col-xs-12">\
            <label>Nombre</label>\
          </div>\
          <div class="col-xs-6 col-sm-3">\
            <div class="form-group">\
              <label for="name1Afectado'+num1+'" class="sr-only">1er Nombre</label>\
              <input type="text" class="form-control" id="name1Afectado'+num1+'" placeholder="José">\
            </div>\
          </div>\
          <div class="col-xs-6 col-sm-3">\
            <div class="form-group">\
              <label for="name2Afectado'+num1+'" class="sr-only"><small>2do Nombre</small></label>\
              <input type="text" class="form-control" id="name2Afectado'+num1+'" placeholder="Manuel">\
            </div>\
          </div>\
          <div class="col-xs-6 col-sm-3">\
            <div class="form-group">\
              <label for="apellido1Afectado'+num1+'" class="sr-only">1er Apellido</label>\
              <input type="text" class="form-control" id="apellido1Afectado'+num1+'" placeholder="Pérez">\
            </div>\
          </div>\
          <div class="col-xs-6 col-sm-3">\
            <div class="form-group">\
              <label for="apellido2Afectado'+num1+'" class="sr-only"><small>2do Apellido</small></label>\
              <input type="text" class="form-control" id="apellido2Afectado'+num1+'" placeholder="Rodríguez">\
            </div>\
          </div>\
        </div>\
        <div class="row">\
          <div class="col-xs-12 col-sm-6">\
            <div class="form-group">\
              <label for="affectionType'+num1+'">Tipo</label>\
              <select class="form-control" id="affectionType'+num1+'">\
                <option value="" selected="selected">Seleccione tipo de afectado</option>\
                <option value="1">Estudiante de la USB</option>\
                <option value="2">Profesor de la USB</option>\
                <option value="3">Empleado de la USB</option>\
                <option value="4">Obrero de la USB</option>\
                <option value="5">Externo</option>\
              </select>\
            </div>\
          </div>\
          <div class="col-xs-8 col-sm-5">\
            <div class="form-group">\
              <label for="affectedCI'+num1+'">Cédula</label>\
              <input type="text" class="form-control" id="affectedCI'+num1+'" placeholder="21.123.123">\
            </div>\
          </div>\
          <div class="col-xs-4 col-sm-1">\
            <div class="form-group">\
              <label for="affectedGender'+num1+'">Sexo</label>\
              <select class="form-control" id="affectedGender'+num1+'">\
                <option value="?" selected="selected">?</option>\
                <option value="F">F</option>\
                <option value="M">M</option>\
              </select>\
            </div>\
          </div>\
        </div>\
        <div class="row">\
          <div class="col-xs-12 col-sm-6">\
            <h3>Contacto</h3>\
            <div id="emailCNT'+num1+'">\
              <label>Correos Electronicos</label>\
              <input class="form-control" id="emailMember'+num1+'-'+num2+'" type="email" placeholder="josebombero@gmail.com" name="emailMember'+num1+'-'+num2+'">\
            </div>\
            <div class="col-xs-12 text-right">\
              <a href="#" id="addEmail'+num1+'" class="addEmail" role="button">\
                <small>Añadir email adicional<span class="glyphicon glyphicon-envelope"></span></small>\
              </a>\
            </div>\
            <div id="phoneCNT'+num1+'">\
              <label>Teléfonos</label>\
              <input class="form-control" id="phoneMember'+num1+'-'+num2+'" type="tel" placeholder="0424-8412323" name="phoneMember'+num1+'-'+num2+'">\
            </div>\
            <div class="col-xs-12 text-right">\
              <a href="#" id="addPhone'+num1+'" class="addPhone" role="button">\
                <small>Añadir teléfono adicional<span class="glyphicon glyphicon-earphone"></span></small>\
              </a>\
            </div>\
          </div>\
          <div class="col-xs-12 col-sm-6">\
            <h3>Notas/Tratamiento</h3>\
            <div class="form-group">\
              <textarea id="affectedNotes'+num1+'" class="form-control" rows="6"></textarea>\
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
