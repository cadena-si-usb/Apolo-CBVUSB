$.formUtils.addValidator({
  name : 'numeroTelefono1',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#telefono-emergencia1').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (expreg.test(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono1'
});

$.formUtils.addValidator({
  name : 'numeroTelefono2',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#telefono-emergencia2').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (expreg.test(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono2'
});

$.formUtils.addValidator({
  name : 'numeroTelefono3',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#tel1').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (expreg.test(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono3'
});

$.formUtils.addValidator({
  name : 'numeroTelefono4',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#tel2').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (expreg.test(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono4'
});

$.formUtils.addValidator({
  name : 'numeroTelefono5',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#tel3').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (expreg.test(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono5'
});

$.formUtils.addValidator({
  name : 'numeroTelefono6',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#tel4').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (expreg.test(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono6'
});

$.formUtils.addValidator({
  name : 'numeroTelefono7',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#tel5').val();
    var expreg = /^\d+$/;
    return ((text.length == 11) && (expreg.test(text)));
  },
  errorMessage : 'El número telefónico debe tener 11 dígitos. Además no debe contener letras o símbolos.',
  errorMessageKey: 'numeroTelefono7'
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