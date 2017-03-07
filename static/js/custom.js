$(document).ready(function() {
    var comissionsCNT = $("#comissionsCNT"); // ID del contenedor de las comisiones
    var addComission = $("#addComission");   // ID del botón para añadir comisiones
    var addUnit = $(".addUnit");             // ID del botón para añadir unidad
    var comissionsCount = 1;
    var unitsCount = [1];

    $(".clickable-row").on('click', function() {
        window.location = $(this).data("href");
    });

    $("body").on("click","a.addUnit", function() {
        var num1 = parseInt(this.id.match(/\d+/g), 10 );
        var unitCNT = "#unitsCNT" + num1;

        unitsCount[num1-1]++;
        var num2 = unitsCount[num1-1];

        $(unitCNT).append(
        '<div id="unit'+num1+'-'+num2+'">\
            <div class="col-xs-4 col-sm-2">\
                <select id="unitValue'+num1+'-'+num2+'" class="form-control" name="unidad">\
                    <option value="" selected="selected">--</option>\
                    <option value="1">A1</option>\
                    <option value="2">M2</option>\
                    <option value="3">L1</option>\
                </select>\
            </div>\
          <div class="col-xs-8 col-sm-10">\
            <input id="comissionDriver'+num1+'-'+num2+'" type="text" class="form-control col-xs-6" placeholder="Conductor" name="conductor">\
          </div>\
        </div>');
    });

    $(addComission).on('click', function() {
        comissionsCount++;
        unitsCount = unitsCount.concat([1]);

        var num1 = comissionsCount;
        var num2 = unitsCount[num1-1];

        $(comissionsCNT).append(
        '<div class="row" id="comission"'+num1+'>\
          <div class="col-xs-12"><h3 id="comissionTitle'+num1+'">Comisión #'+num1+'</h3></div>\
          <div class="col-xs-12 col-sm-6">\
            <div class="form-group ui-widget">\
              <label for="commissionBoss'+num1+'">Jefe de comisión</label>\
              <input id="commissionBoss'+num1+'" type="text" class="form-control" placeholder="Don Quijote" name="jefeComision">\
            </div>\
            <label for="unitTitle">Unidades</label>\
            <div class="row">\
              <div id="unitsCNT'+num1+'">\
                <div id="unit'+num1+'-'+num2+'">\
                  <div class="col-xs-4 col-sm-2">\
                    <select id="unitValue'+num1+'-'+num2+'" class="form-control" name="unidad">\
                      <option value="" selected="selected">--</option>\
                      <option value="1">A1</option>\
                      <option value="2">M2</option>\
                      <option value="3">L1</option>\
                    </select>\
                  </div>\
                  <div class="col-xs-8 col-sm-10">\
                    <input id="comissionDriver'+num1+'-'+num2+'" type="text" class="form-control col-xs-6" placeholder="Conductor" name="conductor">\
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
            <div class="comissionMembers">\
              <label for="comissionMembers'+num1+'">Acompañantes</label>\
              <input type="text" class="form-control" id="comissionMember'+num1+'-0" placeholder="Sancho Panza" name="acompanante0">\
              <input type="text" class="form-control" id="comissionMember'+num1+'-1" placeholder="Sancho Panza" name="acompanante1">\
              <input type="text" class="form-control" id="comissionMember'+num1+'-2" placeholder="Sancho Panza" name="acompanante2">\
            </div>\
            <div class="text-right">\
              <a href="#" id="addComissionMember'+num1+'" role="button">\
                <small>Añadir acompañante <span class="glyphicon glyphicon-user"></span></small>\
              </a>\
            </div>\
          </div>\
        </div>');

    });

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