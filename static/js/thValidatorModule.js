$.formUtils.addValidator({
  name : 'numeroTelefono',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#tlf_msg').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (text.match(expreg)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono'
});

$.formUtils.addValidator({
  name : 'nombreContacto',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#persona_contacto_nombre').val();
    var expreg = /^[0-9a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑ-\s]+$/;;
    return (text.match(expreg));
  },
  errorMessage : 'Debe ser no vacío y contener sólo letras, guiones o espacios.',
  errorMessageKey: 'nombreContacto'
});