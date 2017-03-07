$(document).ready(function(){

  // obtiene el div comisionPrefab en su estado inicial
  var $div = $('div[id^="comisionPrefab"]:last');
  var $comisionPrefab = $div.clone();

  // obtiene el div unidad en su estado inicial
  var $unidad = $('div[id^="i_Unidad"]:last');
  var $unidadPrefab = $unidad.clone();

  $(".clickable-row").click(function() {
    window.location = $(this).data("href");
  });

  $('#instanceComision').click(function(){

    // get the last DIV which ID starts with ^= "comisionPrefab"
    $div = $('div[id^="comisionPrefab"]:last');

    // Read the Number from that DIV's ID (i.e: 3 from "comisionPrefab3")
    // And increment that number by 1
    var num = parseInt( $div.prop("id").match(/\d+/g), 10 ) +1;

    var $comisionPrefab2 = $comisionPrefab.clone();
    // Assign the new ID (i.e: from num 4 to ID "comisionPrefab4")
    $comisionPrefab2.prop('id', 'comisionPrefab'+num);
    $comisionPrefab2.appendTo("#instances");

    // Actualizo el id y el nombre de la comision
    // get the last H3 which ID starts with ^= "t_Comision"
    $h3 = $('h3[id^="t_Comision"]:last');
    $h3.prop('id', 't_Comision'+num );
    $($h3).html("Comision #" + num);

    // Actualizo el id del nuevo boton anadir unidad
    // get the last DIV which ID starts with ^= "comisionPrefab"
    $unidad = $('div[id^="i_Unidad"]:last');
    $unidad.prop('id', 'i_Unidad'+num);
    //$(this).hide();

  });

  //al hacer click en anadir unidad, instacia y
  // anexa una nueva comision vacia al formulario
  //#instanciarUnidad es el id del primer boton "anadir unidad"
  $('#instanciarUnidad').click(function(){

    // get the last DIV which ID starts with ^= "comisionPrefab"
    // obtiene la ultima unidad, pero de todas las que esten instanciadas,
    // eg. puede corresponder a otra comision
    $unidad = $('div[id^="i_Unidad"]:last');
    var num = parseInt( $unidad.prop("id").match(/\d+/g), 10 ) +1;
    var $unidadPrefab2 = $unidadPrefab.clone();

    //var src = $('#i_Unidad'+num); no sirve
    var src = $('#i_Unidad'+1);

    // Assign the new ID (i.e: from num 4 to ID "comisionPrefab4")
    $unidadPrefab2.prop('id', 'i_Unidad'+num);
    $unidadPrefab2.appendTo(src);
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

    }, function(isConfirm){
      if (isConfirm) { form.submit();
        swal("Enviado!",
        "Se ha registrado el servicio satisfatoriamente",
        "success");
      }
    });
  });
});
