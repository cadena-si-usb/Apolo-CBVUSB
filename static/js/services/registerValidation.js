// Validacion de form de registro de servicios
var borrador;

function validateForm() {
    // Si se esta guardando borrador entonces saltar validacion
    if (!borrador) {
        var tipo = document.forms["registro"]["tipo"].value;
        var fechaCreacion = document.forms["registro"]["fechaCreacion"].value;
        //var fechaLlegada  = document.forms["registro"]["fechaLlegada"].value;
        var fechaRegreso  = document.forms["registro"]["fechaFinalizacion"].value;
        var descripcion  = document.forms["registro"]["descripcion"].value;
        var localizacion  = document.forms["registro"]["localizacion"].value;

        var horaCreacion = document.forms["registro"]["horaCreacion"].value;
        var horaRegreso = document.forms["registro"]["horaFinalizacion"].value;
        var validate = true;

        // Verificar no nulidad de campos
        if (fechaCreacion > fechaRegreso || ((fechaRegreso >= fechaCreacion) &&  horaCreacion > horaRegreso)) validate = false;
        if (fechaCreacion < "01/01/1983") validate = false;

        if (validate) swal("Parece que se ingresarón datos incorrectos");

    } else {
        swal("¡Guardado!");
        return true
    }
}

// Colocar en falso para pasar por proceso de validacion de form
function regirterService() {
    borrador = false;
}

// Colocar en verdadero para no hacer validacion de form
function saveDraft() {
    borrador = true;
}