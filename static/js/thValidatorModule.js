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
  name : 'rangoMenu',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('select[name=rango]').val();
    return (text == "");
  },
  errorMessage : 'Debe elegir una opción válida.',
  errorMessageKey: 'rangoMenu'
});

$.formUtils.addValidator({
  name : 'cargoMenu',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('select[name=rango]').val();
    return (text == None);
  },
  errorMessage : 'Debe elegir una opción válida.',
  errorMessageKey: 'cargoMenu'
});

$.formUtils.addValidator({
  name : 'carnetVal',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#carnet').val();
    var expreg = /^\d+$/;
    return ((text >= 0) && (expreg.test(text)));
  },
  errorMessage : 'El carnet es un número positivo.',
  errorMessageKey: 'carnetVal'
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

$.formUtils.addValidator({
  name : 'cedulaVal',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#cedula').val();
    var expreg = /^\d+$/;
    return ((text >= 0) && (expreg.test(text)));
  },
  errorMessage : 'La cédula es un número positivo.',
  errorMessageKey: 'cedulaVal'
});

$.formUtils.addValidator({
  name : 'primerNombreVal',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#primer_nombre').val();
    var expreg = /^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$/;;
    return (expreg.test(text));
  },
  errorMessage : 'Debe ser no vacío y contener sólo letras, guiones o espacios.',
  errorMessageKey: 'primerNombreVal'
});

$.formUtils.addValidator({
  name : 'primerApellidoVal',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#primer_apellido').val();
    var expreg = /^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$/;;
    return (expreg.test(text));
  },
  errorMessage : 'Debe ser no vacío y contener sólo letras, guiones o espacios.',
  errorMessageKey: 'primerApellidoVal'
});


