$(document).ready(function(){
  html2canvas(document.body, {
    onrendered: function(canvas){
      var img = canvas.toDataURL("image/png");
      var doc = new jsPDF("p", "pt", "letter");
      doc.addImage(img, 'JPEG', -80, 50, 795, 400);
      doc.save('Servicio.pdf');
    },
  });
});
