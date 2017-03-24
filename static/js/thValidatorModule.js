$.formUtils.addValidator({
  name : 'numeroTelefono',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#tlf_msg').val();
    var expreg = /^\d+$/;
    return ((text.length == 11 || text.length == 0) && (expreg.test(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono'
});

$.formUtils.addValidator({
  name : 'nombreContacto',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#persona_contacto_nombre').val();
    var expreg = /^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$/;;
    return (expreg.test(text));
  },
  errorMessage : 'Debe ser no vacío y contener sólo letras, guiones o espacios.',
  errorMessageKey: 'nombreContacto'
});