// Validacion de form de registro de servicios
var borrador;

function validateForm() {
    if (!borrador) swal("¡Enviado!");
    else swal("¡Guardado!");
    return true
}

// Colocar en falso para pasar por proceso de validacion de form
function regirterService() {
    borrador = false;
}

// Colocar en verdadero para no hacer validacion de form
function saveDraft() {
    borrador = true;
}