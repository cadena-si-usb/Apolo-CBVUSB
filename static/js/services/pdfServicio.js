$(document).ready(function(){
  var divWidth = $('#export').width();
  var divHeight = $('#export').height();
  html2canvas(document.body, {
    onrendered: function(canvas){
      var img = canvas.toDataURL("image/png");
      var doc = new jsPDF("p", "pt", "letter");

      divWidth = divWidth * 0.90;
      divHeight = divHeight * 0.57;

      doc.addImage(img, 'JPEG', -85, 50, divWidth, divHeight);
      var currentTime = new Date();
      doc.save('Servicio_' + currentTime + '.pdf');
    },
  });
});
