$.formUtils.addValidator({
  name : 'startDateOutOfRange',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#startDate').val().split("/");
    if (text.length == 3) {
      var date = new Date(text[2], text[1]-1, text[0]);
      var minDate = new Date("1983", "01"-1, "01");
      return (date >= minDate);
    } else {
      return true;
    }
  },
  errorMessage : 'La fecha de inicio no puede estar antes del 01/01/1983',
  errorMessageKey: 'startDateOutOfRange'
});

$.formUtils.addValidator({
  name : 'endDateOutOfRange',
  validatorFunction : function(value, $el, config, language, $form) {
    var text = $('#endDate').val().split("/");
    if (text.length == 3) {
      var date = new Date(text[2], text[1]-1, text[0]);
      var minDate = new Date("1983", "01"-1, "01");
      return (date >= minDate);
    } else {
      return true;
    }
  },
  errorMessage : 'La fecha de inicio no puede estar antes del 01/01/1983',
  errorMessageKey: 'endDateOutOfRange'
});

$.formUtils.addValidator({
  name : 'endBeforeStart',
  validatorFunction : function(value, $el, config, language, $form) {
    var text1 = $('#startDate').val().split("/");
    var text2 = $('#startTime').val().split(":");
    var text3 = $('#endDate').val().split("/");
    var text4 = $('#endTime').val().split(":");
    if ((text1.length >= 3) && (text2.length >= 2) && (text3.length >= 3) && (text4.length >= 2)) {
      var startDate = new Date(text1[2], text1[1]-1, text1[0], text2[0], text2[1]);
      var endDate = new Date(text3[2], text3[1]-1, text3[0], text4[0], text4[1]);
      return (startDate < endDate);
    } else {
      return true;
    }
  },
  errorMessage : 'El servicio debe terminar al menos un minuto después de haber empezado',
  errorMessageKey: 'endBeforeStart'
});

$.formUtils.addValidator({
  name : 'incompleteBasicInfo',
  validatorFunction : function(value, $el, config, language, $form) {
    var field1 = $('#tipo').val();
    var field2 = $('#startDate').val();
    var field3 = $('#startTime').val();
    var field4 = $('#endDate').val();
    var field5 = $('#endTime').val();
    var field6 = $('#description').val();
    var field7 = $('#address').val();
    if ((field1.length)&&(field2.length)&&(field3.length)&&(field4.length)&&(field5.length)&&(field6.length)&&(field7.length)) return true;
    else return false;
  },
  errorMessage : 'Hay campos vacíos en la pestaña de información básica',
  errorMessageKey: 'incompleteBasicInfo'
});