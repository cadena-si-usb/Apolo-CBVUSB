var inicio = 1900;
var fin = new Date().getFullYear();
var options = "";
for(var ano = fin ; ano >=inicio; ano--){
  options += "<option>"+ ano +"</option>";
}
document.getElementById("ano").innerHTML = options;