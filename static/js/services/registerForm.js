$(document).ready(function() {
  var commissionsCNT = $("#commissionsCNT");                            // ID del contenedor de las comisiones
  var affectedCNT = $("#affectedCNT");                                  // ID del contenedor de los afectados
  var comExtCNT = $("#comExtCNT");                                      // ID del contenedor de los afectados
  var addCommission = $("#addCommission");                              // ID del botón para añadir comisiones
  var addAffected = $("#addAffected");                                  // ID del botón para añadir Afectados
  var addApoyoExt = $("#addApoyoExt");                                  // ID del botón para añadir Afectados
  var commissionsCount = 1;                                             // Contador de comisiones
  var afectadosCount = 1;                                               // Contador de afectados
  var apoyoExtCount = 1;                                                // Contador de afectados
  var commissionMembersCount = [3];                                     // Arreglo para contar los acompañantes (Por defecto 3)
  var emailsCount = [1];                                                // Arreglo para contar los emails (Por defecto 1)
  var phoneCount = [1];                                                 // Arreglo para contar los Teléfonos (Por defecto 1)
  var unitExtCount = [1];                                               // Arreglo para contar las unidades externas (Por defecto 1)
  var $unitsList = $('select[id^="unitValue"]:last').prop('outerHTML'); // Copia de la lista de unidades

  // Función para los botones para añadir acompañantes
  $("body").on("click","button.addCommissionMember", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );            // Obtener el número de la comisión al que corresponde el acompañante
    var commissionMembersCNT = "#commissionMembersCNT" + num1;  // Generar el identificador al contenedor del acompañante

    commissionMembersCount[num1-1]++;                           // Aumentar el contador de acompañantes para la comisión permitente
    var num2 = commissionMembersCount[num1-1];                  // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(commissionMembersCNT).append(
    '<input list="firefighterList" name="commissionMember'+num1+'-'+num2+'" class="form-control" placeholder="Acompañante de Comisión">');
  });

  // Función para los botones para añadir emails
  $("body").on("click","button.addAffectedEmail", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número del afectado al que corresponde el email
    var emailCNT = "#emailsCNT" + num1;                // Generar el identificador al contenedor de la unidad correspondiente

    emailsCount[num1-1]++;                             // Aumentar el contador de emails para el afectado permitente
    var num2 = emailsCount[num1-1];                    // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(emailCNT).append('<input type="email" class="form-control" id="affectedEmail'+num1+'-'+num2+'" name="affectedEmail'+num1+'-'+num2+'" data-validation="email" placeholder="mail@website.com">');
  });

  // Función para los botones para añadir phones
  $("body").on("click","button.addAffectedPhone", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número del afectado al que corresponde el phone
    var phoneCNT = "#phonesCNT" + num1;                // Generar el identificador al contenedor de la unidad correspondiente

    phoneCount[num1-1]++;                              // Aumentar el contador de phones para el afectado permitente
    var num2 = phoneCount[num1-1];                     // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(phoneCNT).append('<input type="tel" class="form-control" id="affectedPhone'+num1+'-'+num2+'" name="affectedPhone'+num1+'-'+num2+'" data-validation="length" data-validation-length="12-20" data-validation="number" data-validation-allowing="-+()" placeholder="Teléfono/Celular">');
  });

  // Función para los botones para añadir unidades externas
  $("body").on("click","button.addUnitExt", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número del afectado al que corresponde el phone
    var unitExtCNT = "#unitExtCNT" + num1;             // Generar el identificador al contenedor de la unidad correspondiente

    unitExtCount[num1-1]++;                            // Aumentar el contador de phones para el afectado permitente
    var num2 = unitExtCount[num1-1];                   // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(unitExtCNT).append(
    '<div id="unitExt'+num1+'-'+num2+'">\
      <div class="col-xs-6 col-sm-6">\
        <label for="unitExtValue'+num1+'-'+num2+'">Unidades</label>\
        <input id="unitExtValue'+num1+'-'+num2+'" type="text" class="form-control" placeholder="Unidad" name="unitExtValue'+num1+'-'+num2+'">\
      </div>\
      <div class="col-xs-6 col-sm-6">\
        <label for="unitExtValue'+num1+'-'+num2+'">Placa Unidad</label>\
        <input id="unitExtPlaca'+num1+'-'+num2+'" type="text" class="form-control col-xs-6" placeholder="Conductor" name="unitExtPlaca'+num1+'-'+num2+'">\
      </div>\
    </div>');
  });

  // Función para el botón para añadir nuevas comisiones
  $(addCommission).on('click', function() {
    commissionsCount++;                                           // Aumentar el contador de comisiones
    commissionMembersCount = commissionMembersCount.concat([3]);  // Agregar un nuevo slot contador de acompañantes

    var num1 = commissionsCount;                                  // Variable auxiliar para la sustitucion en el html de abajo
    var num2 = 1;                                                 // Variable auxiliar para la sustitucion en el html de abajo

    // Copio la lista de unidades y la formateo para la nueva comisión
    var unitsListCopy = $unitsList.replace(
    '<select id="unitValue1-1" class="form-control" name="unitValue1-1">',
    '<select id="unitValue'+num1+'-'+num2+'" class="form-control" name="unitValue'+num1+'-'+num2+'">');

    // Inserción del html
    $(commissionsCNT).append(
    '<div id="commission'+num1+'">\
      <div class="row">\
        <div class="col-xs-12">\
          <h3 id="commissionTitle'+num1+'" name="commissionTitle'+num1+'">Comisión <kbd>'+num1+'</kbd></h3>\
          <input type="hidden" name="commissionTitle'+num1+'" value="commissionTitle'+num1+'">\
        </div>\
      </div>\
      <div class="row">\
        <div class="col-xs-12 col-sm-4">\
          <div class="form-group ui-widget">\
            <label for="commissionBoss'+num1+'">Jefe de comisión *</label>\
            <input list="firefighterList" name="commissionBoss'+num1+'" class="form-control" data-validation="required" placeholder="Jefe de Comisión">\
          </div>\
          <label for="unitTitle">Unidades</label>\
          <div class="row">\
            <div id="unitsCNT'+num1+'">\
              <div id="unit'+num1+'-'+num2+'">\
                <div class="col-xs-4 col-sm-2">\
                '+unitsListCopy+'\
                </div>\
                <div class="col-xs-8 col-sm-10">\
                  <input list="firefighterList" name="commissionDriver'+num1+'-'+num2+'" class="form-control" placeholder="Conductor">\
                 </div>\
                </div>\
              </div>\
            </div>\
          </div>\
          <div class="col-xs-12 col-sm-4">\
            <div id="commissionMembersCNT'+num1+'">\
              <label for="commissionMember'+num1+'">Acompañantes</label>\
              <input list="firefighterList" name="commissionMember'+num1+'-1" class="form-control" placeholder="Acompañante de Comisión">\
              <input list="firefighterList" name="commissionMember'+num1+'-2" class="form-control" placeholder="Acompañante de Comisión">\
              <input list="firefighterList" name="commissionMember'+num1+'-3" class="form-control" placeholder="Acompañante de Comisión">\
            </div>\
            <div class="text-right">\
              <button id="addCommissionMember'+num1+'" type="button" class="btn bg-primary addCommissionMember top-space-separator addCommissionMember">\
                <small>Añadir acompañante <span class="glyphicon glyphicon-user"></span></small>\
              </button>\
            </div>\
          </div>\
        </div>\
      </div>\
      <hr>');
  });

  // Función para el botón para añadir afectados adicionales
  $(addAffected).on('click', function() {
    afectadosCount++;                      // Aumentar el contador de afectados
    emailsCount = emailsCount.concat([1]); // Agregar un nuevo slot contador de emails
    phoneCount = phoneCount.concat([1]);   // Agregar un nuevo slot contador de phones

    var num1 = afectadosCount;             // Variable auxiliar para la sustitucion en el html de abajo
    var num2 = emailsCount[num1-1];        // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(affectedCNT).append(
      '<div id="affected'+num1+'">\
        <div class="row">\
          <div class="col-xs-12 col-sm-6">\
            <div class="row">\
              <div class="col-xs-12 col-sm-12">\
                <h3>Afectado <kbd>'+num1+'</kbd></h3>\
                <input type="hidden" name="affectedTitle'+num1+'" value="affectedTitle'+num1+'">\
                <label>Nombre *</label>\
              </div>\
              <div class="col-xs-6 col-sm-4 form-group">\
                <input type="text" class="form-control" id="affectedFirstName'+num1+'" name="affectedFirstName'+num1+'" data-validation="required" placeholder="Primer Nombre *">\
              </div>\
              <!--<div class="col-xs-6 col-sm-2 form-group">\
              <label for="affected'+num1+'" class="sr-only"><small>2do Nombre</small></label>\
              <input type="text" class="form-control" id="affectedSecondName'+num1+'" name="affectedSecondName'+num1+'" placeholder="Segundo Nombre">\
            </div>-->\
            <div class="col-xs-6 col-sm-4 form-group">\
              <!--  <label for="affected2" class="sr-only">1er Apellido</label>-->\
              <input type="text" class="form-control" id="affectedFirstSurname'+num1+'" name="affectedFirstSurname'+num1+'" data-validation="required" placeholder="Primer Apellido *">\
            </div>\
            <div class="col-xs-6 col-sm-4 form-group">\
              <label for="affectedName3" class="sr-only"><small>2do Apellido</small></label>\
              <input type="text" class="form-control" id="affectedSecondSurname'+num1+'" name="affectedSecondSurname'+num1+'" placeholder="Segundo Apellido">\
            </div>\
          </div>\
          <div class="row">\
            <div class="col-xs-12 col-sm-4 form-group">\
              <label for="affectedCI'+num1+'">Cedula *</label>\
              <input type="text" class="form-control" id="affectedCI'+num1+'" name="affectedCI'+num1+'" data-validation="required" data-validation="number" placeholder="Número de Cedula">\
            </div>\
            <div class="col-xs-4 col-sm-2">\
              <div class="form-group">\
                <label for="affectedGender'+num1+'">Sexo *</label>\
                <select class="form-control" id="affectedGender'+num1+'" data-validation="required" name="affectedGender'+num1+'">\
                  <option value="?" selected="selected">?</option>\
                  <option value="F">F</option>\
                  <option value="M">M</option>\
                </select>\
              </div>\
            </div>\
          </div>\
          <div class="row">\
            <div class="col-xs-12 col-sm-6 form-group">\
              <label for="affectedType'+num1+'">Tipo *</label>\
              <select class="form-control" id="affectedType'+num1+'" name="affectedType'+num1+'" data-validation="required">\
                <option value="" selected="selected">Seleccione tipo de afectado</option>\
                <option value="1">Estudiante de la USB</option>\
                <option value="2">Profesor de la USB</option>\
                <option value="3">Empleado de la USB</option>\
                <option value="4">Obrero de la USB</option>\
                <option value="5">Externo</option>\
              </select>\
            </div>\
          </div>\
          <div class="row">\
            <div class="col-xs-12 col-sm-6">\
              <div id="emailsCNT'+num1+'">\
                <label for="emailsTitle">Correos Electrónicos</label>\
                <input type="email" class="form-control" id="affectedEmail'+num1+'-'+num2+'" name="affectedEmail'+num1+'-'+num2+'" data-validation="email" placeholder="mail@website.com">\
              </div>\
              <div class="text-right">\
                <button id="addAffectedEmail'+num1+'" type="button" class="btn  addAffectedEmail top-space-separator">+ <span class="glyphicon glyphicon-envelope"></span></button>\
              </div>\
            </div>\
            <div class="col-xs-12 col-sm-6">\
              <div id="phonesCNT'+num1+'">\
                <label for="phonesTitle">Teléfonos</label>\
                <input type="tel" class="form-control" id="affectedPhone'+num1+'-'+num2+'" name="affectedPhone'+num1+'-'+num2+'" data-validation="length" data-validation-length="12-20" data-validation="number" data-validation-allowing="-+()" placeholder="Teléfono/Celular">\
              </div>\
              <div class="text-right">\
                <button id="addAffectedPhone'+num1+'" type="button" class="btn  addAffectedPhone top-space-separator">+ <span class="glyphicon glyphicon-earphone"></span></button>\
              </div>\
            </div>\
          </div>\
        </div>\
        <div class="col-xs-6 col-sm-5 col-sm-offset-1">\
          <br />\
          <br />\
          <br />\
          <label>Notas/Tratamiento</label>\
          <div class="form-group">\
            <textarea id="affectedNotes'+num1+'" name="affectedNotes'+num1+'" class="form-control" data-validation="length" data-validation-length="max700" rows="10"></textarea>\
          </div>\
        </div>\
      </div>\
    </div>\
    <hr>');
  });

  // Función para el botón para añadir afectados adicionales
  $(addApoyoExt).on('click', function() {
    apoyoExtCount++;                         // Aumentar el contador de afectados
    unitExtCount = unitExtCount.concat([1]); // Agregar un nuevo slot contador de emails

    var num1 = apoyoExtCount;                // Variable auxiliar para la sustitucion en el html de abajo
    var num2 = unitExtCount[num1-1];         // Variable auxiliar para la sustitucion en el html de abajo

    $(comExtCNT).append(
      '<div id="comisionExt'+num1+'" class="col-xs-12 col-sm-12">\
      <h3 id="comisionExtTitle'+num1+'" name="comisionExtTitle'+num1+'">Comisión Externa <kbd>'+num1+'</kbd></h3>\
      <input type="hidden" name="comisionExtTitle'+num1+'" value="comisionExtTitle'+num1+'">\
      <div class="form-group ui-widget col-xs-12 col-sm-12">\
        <label for="cuerpoDepartamento'+num1+'">Cuerpo o Departamento</label>\
        <input id="cuerpoDepartamento'+num1+'" type="text" class="form-control" placeholder="Nombre del Departamento" name="cuerpoDepartamento'+num1+'">\
      </div>\
      <div class="form-group ui-widget col-xs-12 col-sm-7">\
        <label for="jefe'+num1+'">Jefe</label>\
        <input id="jefe'+num1+'" type="text" class="form-control" placeholder="Nombre" name="jefe'+num1+'">\
      </div>\
      <div class="col-xs-12 col-sm-5">\
        <label for="cuerpoDepartamento'+num1+'">Número de acompañantes</label>\
        <input id="cuerpoDepartamento'+num1+'" type="text" class="form-control" placeholder="Número" name="cuerpoDepartamento'+num1+'">\
      </div>\
      <div id="unitExtCNT'+num1+'">\
        <div id="unitExt'+num1+'-'+num2+'">\
          <div class="col-xs-6 col-sm-6">\
            <label for="unitExtValue'+num1+'-'+num2+'">Unidades</label>\
            <input id="unitExtValue'+num1+'-'+num2+'" type="text" class="form-control" placeholder="Unidad" name="unitExtValue'+num1+'-'+num2+'">\
          </div>\
          <div class="col-xs-6 col-sm-6">\
            <label for="unitExtValue'+num1+'-'+num2+'">Placa Unidad</label>\
            <input id="unitExtPlaca'+num1+'-'+num2+'" type="text" class="form-control col-xs-6" placeholder="Conductor" name="unitExtPlaca'+num1+'-'+num2+'">\
          </div>\
        </div>\
      </div>\
      <div class="col-xs-12 text-right">\
        <button id="addUnitExt'+num1+'" type="button" class="btn btn-default btn-sm addUnitExt top-space-separator">\
          <small>Añadir unidad externa<span class="glyphicon glyphicon-wrench"></span></small>\
        </button>\
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
        cancelButtonText: "Aún no termino",
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

  // initialize input widgets first
  $('#jqueryExample .time').timepicker({
    'showDuration': true,
    'timeFormat': 'g:ia'
  });

  $('#jqueryExample .date').datepicker({
    'format': 'm/d/yyyy',
    'autoclose': true
  });

  // initialize datepair
  $('#jqueryExample').datepair();
});
