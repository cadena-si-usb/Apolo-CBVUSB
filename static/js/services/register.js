// Validacion de form de registro de servicios
var borrador;

function validateForm() {

    // Si se esta guardando borrador entonces saltar validacion
    if (borrador) {
        return true;
    }

    var tipo = document.forms["registro"]["tipo"].value;
    var fechaCreacion = document.forms["registro"]["fechaCreacion"].value;
    //var fechaLlegada  = document.forms["registro"]["fechaLlegada"].value;
    var fechaRegreso  = document.forms["registro"]["fechaFinalizacion"].value;
    var descripcion  = document.forms["registro"]["descripcion"].value;
    var localizacion  = document.forms["registro"]["localizacion"].value;

    // Verificar no nulidad de campos
    if (tipo == "") {
        alert("ALERTA: Ingrese tipo de servicio")
        return false
    }
    if (fechaCreacion == "") {
        alert("ALERTA: Ingrese fecha de creación de servicio")
        return false
    }
    if (fechaRegreso == "") {
        alert("ALERTA: Ingrese fecha de regreso de servicio")
        return false
    }
    if (descripcion == "") {
        alert("ALERTA: Ingrese descripción de servicio")
        return false
    }
    if (localizacion == "") {
        alert("ALERTA: Ingrese localización de servicio")
        return false
    }

    //if (fechaCreacion > fechaRegreso) {
    //    alert("ALERTA: Fecha de inicio debe debe ser menor o igual a fecha de finalización.");
    //    return false;
    //}
    //if (fechaLlegada > fechaRegreso) {
    //    alert("ALERTA: Fecha de llegada debe debe ser menor o igual a fecha de regreso.");
    //    return false;
    //}
}

// Colocar en falso para pasar por proceso de validacion de form
function regirterService() {
    borrador = false;
}

// Colocar en verdadero para no hacer validacion de form
function saveDraft() {
    borrador = true;
}