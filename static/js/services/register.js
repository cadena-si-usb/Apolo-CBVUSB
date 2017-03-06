// Validacion de form de registro de servicios
function validateForm() {

    var fechaCreacion = document.forms["registro"]["fechaCreacion"].value;
    //var fechaLlegada  = document.forms["registro"]["fechaLlegada"].value;
    var fechaRegreso  = document.forms["registro"]["fechaFinalizacion"].value;
    var descripcion  = document.forms["registro"]["descripcion"].value;
    var localizacion  = document.forms["registro"]["localizacion"].value;
    
    // Verificar no nulidad de campos
    if(fechaCreacion == "") {
    	alert("ALERTA: Ingrese fecha de inicio de servicio.")
    	return false
    }

    //if(fechaLlegada == "") {
    //	alert("ALERTA: Ingrese fecha de llegada de servicio.")
    //	return false
    //}
    if(fechaRegreso == "") {
    	alert("ALERTA: Ingrese fecha de regreso de servicio.")
    	return false
    }
    if(descripcion == "") {
    	alert("ALERTA: Ingrese descripción de servicio.")
    	return false
    }
    if(localizacion == "") {
    	alert("ALERTA: Ingrese dirección de servicio.")
    	return false
    }

    if (fechaCreacion > fechaRegreso) {
        alert("ALERTA: Fecha de inicio debe debe ser menor o igual a fecha de finalización.");
        return false;
    }
    //if (fechaLlegada > fechaRegreso) {
    //    alert("ALERTA: Fecha de llegada debe debe ser menor o igual a fecha de regreso.");
    //    return false;
    //}
}

$( function() {
    $( "#commissionBoss" ).autocomplete({source: nombres});
});