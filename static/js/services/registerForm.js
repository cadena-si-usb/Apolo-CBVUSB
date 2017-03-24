var borrador = false;
function registerService() {$('#draft').val("0");};
function saveDraft() {$('#draft').val("1");};

$(document).ready(function() {
  var commissionsCNT = $("#commissionsCNT");                            // ID del contenedor de las comisiones
  var affectedCNT = $("#affectedCNT");                                  // ID del contenedor de los afectados
  var apoyoExtCNT = $("#comExtCNT");                                    // ID del contenedor de los afectados
  var addCommission = $("#addCommission");                              // ID del botón para añadir comisiones
  var addAffected = $("#addAffected");                                  // ID del botón para añadir Afectados
  var addApoyoExt = $("#addApoyoExt");                                  // ID del botón para añadir Afectados
  var commissionsCount = 1;                                             // Contador de comisiones
  var affectedCount = 0;                                                // Contador de afectados
  var apoyoExtCount = 0;                                                // Contador de afectados
  var commissionMembersCount = [3];                                     // Arreglo para contar los acompañantes (Por defecto 3)
  var emailsCount = [0];                                                // Arreglo para contar los emails (Por defecto 0)
  var liveEmailsCount = [0];                                            // Arreglo para contar los emails actuales (Por defecto 0)
  var phoneCount = [0];                                                 // Arreglo para contar los Teléfonos (Por defecto 0)
  var $unitsList = $('select[id^="unitValue"]:last').prop('outerHTML'); // Copia de la lista de unidades

  // Función para los botones de eliminar comisión
  $(commissionsCNT).on("click","button.removeGroup", function() {
    var $parent = $($($($($(this).parent('span')).parent('div')).parent('div')).parent('div')).parent('div');
    $parent.remove();
  });

  // Función para los botones de eliminar afectado
  $(affectedCNT).on("click","button.removeGroup", function() {
    var $parent = $($($($(this).parent('span')).parent('div')).parent('div')).parent('div');
    $parent.remove();
  });

  // Función para los botones de eliminar apoyo externo
  $(apoyoExtCNT).on("click","button.removeGroup", function() {
    var $parent = $($($(this).parent('span')).parent('div')).parent('div');
    $parent.remove();
  });

  // Función para los botones de eliminar campos simples
  $("body").on("click","button.removeField", function() {
    var $parent = $($(this).parent('span')).parent('div');
    var parentClass = $parent.attr("class");
    var num1 = parseInt($parent.parent('div').attr("id").match(/\d+/g), 10);
    $parent.remove();
    if (~parentClass.indexOf("affectedEmailField")) liveEmailsCount[num1-1]--;
  });

  // Función para los botones de eliminar unidad de apoyo externo
  $("body").on("click","button.removeUnitExt", function() {
    var $parent = $($(this).parent('div')).parent('div');
    $parent.remove();
  });

  // Función para los botones para añadir acompañantes
  $("body").on("click","button.addCommissionMember", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10);             // Obtener el número de la comisión al que corresponde el acompañante
    var commissionMembersCNT = "#commissionMembersCNT" + num1;  // Generar el identificador al contenedor del acompañante
    var htmlCount = "commissionMembersCount" + num1;            // Generar identificador del contador de acompañantes en el html

    commissionMembersCount[num1-1]++;                           // Aumentar el contador de acompañantes para la comisión correspondiente
    var num2 = commissionMembersCount[num1-1];                  // Variable auxiliar para la sustitucion en el html de abajo
    $('input[name='+htmlCount+']').val(num2);                   // Actualizar el contador de acompañantes en el html

    // Inserción del html
    $(commissionMembersCNT).append(
    '<div class="input-group">\
      <input list="firefighterList" name="commissionMember'+num1+'-'+num2+'" class="form-control" data-validation="validName" data-validation-optional="true" placeholder="Acompañante de Comisión">\
      <span class="input-group-btn">\
        <button class="removeButton removeField" type="button" title="Eliminar"><span class="glyphicon glyphicon-remove"></span></button>\
      </span>\
    </div>');
  });

  // Función para los botones para añadir emails
  $("body").on("click","button.addAffectedEmail", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10);      // Obtener el número del afectado al que corresponde el email
    if (liveEmailsCount[num1-1] < 2) {
      var emailCNT = "#emailsCNT" + num1;                // Generar el identificador al contenedor de la unidad correspondiente
      var htmlCount = "emailsCount" + num1;              // Generar identificador del contador de correos en el html

      emailsCount[num1-1]++;                             // Aumentar el contador de emails para el afectado correspondiente
      liveEmailsCount[num1-1]++;                         // Aumentar el contador de emails vivos para el afectado correspondiente
      var num2 = emailsCount[num1-1];                    // Variable auxiliar para la sustitucion en el html de abajo
      $('input[name='+htmlCount+']').val(num2);          // Actualizar el contador de acompañantes en el html

      // Inserción del html
      $(emailCNT).append(
      '<div class="affectedEmailField input-group">\
        <input type="text" class="form-control" id="affectedEmail'+num1+'-'+num2+'" name="affectedEmail'+num1+'-'+num2+'" data-validation="email" data-validation-optional="true" placeholder="mail@website.com">\
        <span class="input-group-btn">\
          <button class="removeButton removeField" type="button" title="Eliminar"><span class="glyphicon glyphicon-remove"></span></button>\
        </span>\
      </div>');
    }
  });

  // Función para los botones para añadir teléfonos
  $("body").on("click","button.addAffectedPhone", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10);    // Obtener el número del afectado al que corresponde el phone
    var phoneCNT = "#phonesCNT" + num1;                // Generar el identificador al contenedor del teléfono
    var htmlCount = "phoneCount" + num1;               // Generar identificador del contador de teléfono en el html

    phoneCount[num1-1]++;                              // Aumentar el contador de teléfono para el afectado correspondiente
    var num2 = phoneCount[num1-1];                     // Variable auxiliar para la sustitucion en el html de abajo
    $('input[name='+htmlCount+']').val(num2);          // Actualizar el contador de acompañantes en el html

    // Inserción del html
    $(phoneCNT).append(
    '<div class="input-group">\
      <input type="tel" class="form-control" id="affectedPhone'+num1+'-'+num2+'" name="affectedPhone'+num1+'-'+num2+'" data-validation="number, length" data-validation-length="10-20" data-validation-optional="true" placeholder="Teléfono/Celular">\
      <span class="input-group-btn">\
        <button class="removeButton removeField" type="button" title="Eliminar"><span class="glyphicon glyphicon-remove"></span></button>\
      </span>\
    </div>');
  });

  // Función para el botón para añadir nuevas comisiones
  $(addCommission).on('click', function() {
    commissionsCount++;                                           // Aumentar el contador de comisiones
    $('input[name=commissionsCount]').val(commissionsCount);      // Actualizar el contador de comisiones en el html
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
      <input type="hidden" name="commissionMembersCount'+num1+'" value="3">\
      <div class="row">\
        <div class="col-xs-12 col-sm-8">\
          <div class="input-group">\
            <h3 id="commissionTitle'+num1+'" name="commissionTitle'+num1+'">Comisión <kbd>'+num1+'</kbd></h3>\
            <span class="input-group-btn">\
              <button class="removeButton removeGroup" type="button">\
                <span>Eliminar comisión </span>\
                <span class="glyphicon glyphicon-remove"></span>\
              </button>\
            </span>\
          </div>\
          <input type="hidden" name="commissionTitle'+num1+'" value="commissionTitle'+num1+'">\
        </div>\
      </div>\
      <div class="row">\
        <div class="col-xs-12 col-sm-4">\
          <div class="form-group">\
            <label for="commissionBoss'+num1+'">Jefe de comisión</label>\
            <input list="firefighterList" name="commissionBoss'+num1+'" class="form-control" data-validation="validName" data-validation-optional="true" placeholder="Jefe de Comisión">\
          </div>\
          <label for="unitTitle">Unidad</label>\
          <div class="row">\
            <div id="unitsCNT'+num1+'">\
              <div id="unit'+num1+'-'+num2+'">\
                <div class="col-xs-4 col-sm-4">\
                '+unitsListCopy+'\
                </div>\
                <div class="col-xs-8 col-sm-8">\
                  <input list="firefighterList" name="commissionDriver'+num1+'-'+num2+'" class="form-control" data-validation="validName" data-validation-optional="true" placeholder="Conductor">\
                 </div>\
                </div>\
              </div>\
            </div>\
          </div>\
          <div class="col-xs-12 col-sm-4">\
            <div id="commissionMembersCNT'+num1+'">\
              <label for="commissionMember'+num1+'">Acompañantes</label>\
              <div class="input-group">\
                <input list="firefighterList" name="commissionMember'+num1+'-1" class="form-control" data-validation="validName" data-validation-optional="true" placeholder="Acompañante de Comisión">\
                <span class="input-group-btn">\
                  <button class="removeButton removeField" type="button" title="Eliminar"><span class="glyphicon glyphicon-remove"></span></button>\
                </span>\
              </div>\
              <div class="input-group">\
                <input list="firefighterList" name="commissionMember'+num1+'-2" class="form-control" data-validation="validName" data-validation-optional="true" placeholder="Acompañante de Comisión">\
                <span class="input-group-btn">\
                  <button class="removeButton removeField" type="button" title="Eliminar"><span class="glyphicon glyphicon-remove"></span></button>\
                </span>\
              </div>\
              <div class="input-group">\
                <input list="firefighterList" name="commissionMember'+num1+'-3" class="form-control" data-validation="validName" data-validation-optional="true" placeholder="Acompañante de Comisión">\
                <span class="input-group-btn">\
                  <button class="removeButton removeField" type="button" title="Eliminar"><span class="glyphicon glyphicon-remove"></span></button>\
                </span>\
              </div>\
            </div>\
            <div class="text-right">\
              <button id="addCommissionMember'+num1+'" type="button" class="btn bg-1 addCommissionMember top-space-separator addCommissionMember">\
                Añadir acompañante  <span class="glyphicon glyphicon-user"></span>\
              </button>\
            </div>\
          </div>\
        </div>\
        <hr>\
      </div>');
  });

  // Función para el botón para añadir afectados
  $(addAffected).on('click', function() {
    affectedCount++;                                   // Aumentar el contador de afectados
    $('input[name=affectedCount]').val(affectedCount); // Actualizar el contador de afectados en el html
    emailsCount = emailsCount.concat([0]);             // Agregar un nuevo slot al contador de emails
    liveEmailsCount = liveEmailsCount.concat([0]);     // Agregar un nuevo slot al contador de emails vivos
    phoneCount = phoneCount.concat([0]);               // Agregar un nuevo slot al contador de phones
    var num1 = affectedCount;                          // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(affectedCNT).append(
    '<div id="affected'+num1+'">\
      <input type="hidden" name="emailsCount'+num1+'" value="0">\
      <input type="hidden" name="phoneCount'+num1+'" value="0">\
      <div class="row">\
        <div class="input-group text-right no-space-bottom">\
          <span class="input-group-btn">\
            <button class="removeButton removeGroup" type="button">\
              <span>Eliminar afectado</span>\
              <span class="glyphicon glyphicon-remove"></span>\
            </button>\
          </span>\
        </div>\
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
            <label for="affectedCI'+num1+'">Cédula</label>\
            <input type="text" class="form-control" id="affectedCI'+num1+'" name="affectedCI'+num1+'" data-validation="number" data-validation-allowing="range[1;99000000]" data-validation-optional="true" placeholder="Número de Cedula">\
          </div>\
          <div class="col-xs-4 col-sm-2">\
            <div class="form-group">\
              <label for="affectedGender'+num1+'">Sexo</label>\
              <select class="form-control" id="affectedGender'+num1+'" data-validation="required" name="affectedGender'+num1+'">\
                <option value="-" selected="selected">-</option>\
                <option value="F">F</option>\
                <option value="M">M</option>\
              </select>\
            </div>\
          </div>\
        </div>\
        <div class="row">\
          <div class="col-xs-12 col-sm-6 form-group">\
            <label for="affectedType'+num1+'">Tipo</label>\
            <select class="form-control" id="affectedType'+num1+'" name="affectedType'+num1+'">\
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
            </div>\
            <div class="text-right">\
              <button id="addAffectedEmail'+num1+'" type="button" class="btn bg-1 addAffectedEmail top-space-separator">+ <span class="glyphicon glyphicon-envelope"></span></button>\
            </div>\
          </div>\
          <div class="col-xs-12 col-sm-6">\
            <div id="phonesCNT'+num1+'">\
              <label for="phonesTitle">Teléfonos</label>\
            </div>\
            <div class="text-right">\
              <button id="addAffectedPhone'+num1+'" type="button" class="btn bg-1 addAffectedPhone top-space-separator">+ <span class="glyphicon glyphicon-earphone"></span></button>\
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
    <hr>\
  </div>');
  });

  // Función para el botón para añadir apoyo externo
  $(addApoyoExt).on('click', function() {
    apoyoExtCount++;                                   // Aumentar el contador de apoyo externo
    $('input[name=apoyoExtCount]').val(apoyoExtCount); // Actualizar el contador de apoyo externo en el html
    var num1 = apoyoExtCount;                          // Variable auxiliar para la sustitucion en el html de abajo

    $(apoyoExtCNT).append(
    '<div id="comExt'+num1+'">\
      <div class="input-group text-right no-space-bottom">\
        <span class="input-group-btn">\
          <button class="removeButton removeGroup" type="button">\
            <span>Eliminar apoyo externo</span>\
            <span class="glyphicon glyphicon-remove"></span>\
          </button>\
        </span>\
      </div>\
      <div class="row">\
        <div class="col-xs-12 col-sm-6">\
          <div id="comisionExt'+num1+'" class="col-xs-12 col-sm-12">\
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
              <input id="numAcomp'+num1+'" type="text" class="form-control" data-validation="number" data-validation-optional="true" placeholder="Número" name="numAcomp'+num1+'">\
            </div>\
            <div id="unitExtCNT'+num1+'">\
              <div id="unitExt'+num1+'">\
                <div class="col-xs-6 col-sm-6">\
                  <label for="unitExtValue'+num1+'">Unidad</label>\
                  <input id="unitExtValue'+num1+'" type="text" class="form-control" placeholder="Unidad" name="unitExtValue'+num1+'">\
                </div>\
                <div class="col-xs-6 col-sm-6">\
                  <label for="unitExtValue'+num1+'">Placa Unidad</label>\
                  <input id="unitExtPlaca'+num1+'" type="text" class="form-control col-xs-6" placeholder="Conductor" name="unitExtPlaca'+num1+'">\
                </div>\
              </div>\
            </div>\
          </div>\
        </div>\
        <div class="col-xs-6 col-sm-5 col-sm-offset-1">\
          <br />\
          <br />\
          <br />\
          <label>Comentario</label>\
          <div class="form-group">\
            <textarea id="unitExtNotes'+num1+'" name="unitExtNotes'+num1+'" class="form-control" data-validation="length" data-validation-length="max700" rows="10"></textarea>\
          </div>\
        </div>\
      </div>\
      <hr>\
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
      closeOnConfirm: true,
      html: false
    }, function(isConfirm) {
        if (isConfirm) {
          // Enviar form
          form.submit();
        }
    });
  });

  // Función para popUp al momento guardar el borrador
  $('#btn-draft').on('click',function(e){
    e.preventDefault();
    var form = $('#registro');
    swal({
      title: "¿Desea agregar este servicio a sus borradores?",
      text: "Podrá terminar el registro del servicio en otro momento",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#1565C0",
      confirmButtonText: "¡Si, guardar!",
      cancelButtonText: "Aún no termino",
      closeOnConfirm: false,
      html: false
    }, function(isConfirm) {
      if (isConfirm) {
        // Deshabilitar las validaciones de nulidad
        $('#tipo').removeAttr('data-validation');
        $('#startDate').removeAttr('data-validation');
        $('#startTime').removeAttr('data-validation');
        $('#endDate').removeAttr('data-validation');
        $('#endTime').removeAttr('data-validation');
        $('#description').removeAttr('data-validation');
        $('#address').removeAttr('data-validation');
        $('#commissionBoss1').removeAttr('data-validation');

        // Enviar form
        form.submit();

        // Popup
        swal("¡Guardado!", "", "success");
      }
    });
  });

  // Función para popUp al momento de cancelar el registro
  $('#btn-cancel').on('click',function(e){
    e.preventDefault();
    swal({
      title: "¿Está seguro de que desea cancelar el registro?",
      text: "Toda la información de este registro se descartará",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "¡Si, cancelar!",
      cancelButtonText: "Voy a darle otra oportunidad",
      closeOnConfirm: false,
      html: false
    }, function(isConfirm) {
      if (isConfirm) {
        // Popup
        swal({
          title: "Registro cancelado",
          text: "",
        });

        // Redireccionar al index de servicios
        window.location.replace($('#btn-cancel').attr("name"));
      }
    });
  });

  // initialize input widgets first
  $('#start-end-date .time').timepicker({
    'scrollDefault': 'now',
    'timeFormat': 'H:i',
    'forceRoundTime': false
  });

  $('#start-end-date .date').datepicker({
    'format': 'dd/mm/yyyy',
    'autoclose': true
  });

  // initialize datepair
  $('#start-end-date').datepair();

});
