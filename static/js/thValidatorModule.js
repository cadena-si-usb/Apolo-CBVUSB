$.formUtils.addValidator({
  name : 'numeroTelefono',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#tlf_msg').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (expreg.text(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono'
});