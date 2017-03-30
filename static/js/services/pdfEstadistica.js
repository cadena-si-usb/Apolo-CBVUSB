$(document).ready(function(){
  var divWidth = $('#export').width();
  var divHeight = $('#export').height();
  html2canvas(document.body, {
    onrendered: function(canvas){
      var img = canvas.toDataURL("image/png");
      var doc = new jsPDF("p", "pt", "letter");

      divWidth = divWidth * 0.90;
      divHeight = divHeight * 0.50;

      //doc.addImage(img, 'JPEG', -90, 50, divWidth, divHeight);
      doc.addImage(img, 'JPEG', -90, 50, 795, 380);
      var currentTime = new Date();
      doc.save('Estadistica_' + currentTime + '.pdf');
    },
  });
});
