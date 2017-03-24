var inicio = 1900;
var fin = new Date().getFullYear();
var options = "";
for(var ano = fin ; ano >=inicio; ano--){
  options += "<option>"+ ano +"</option>";
}
document.getElementById("ano").innerHTML = options;

if (mesS == "Todos") {
	$('[name=mes]').val(0);	
} else if (mesS == "Enero") {
	$('[name=mes]').val(1);	
} else if (mesS == "Febrero") {
	$('[name=mes]').val(2);	
} else if (mesS == "Marzo") {
	$('[name=mes]').val(3);	
} else if (mesS == "Abril") {
	$('[name=mes]').val(4);	
} else if (mesS == "Mayo") {
	$('[name=mes]').val(5);	
} else if (mesS == "Junio") {
	$('[name=mes]').val(6);	
} else if (mesS == "Julio") {
	$('[name=mes]').val(7);	
} else if (mesS == "Agosto") {
	$('[name=mes]').val(8);	
} else if (mesS == "Septiembre") {
	$('[name=mes]').val(9);	
} else if (mesS == "Octubre") {
	$('[name=mes]').val(10);	
} else if (mesS == "Noviembre") {
	$('[name=mes]').val(11);	
} else if (mesS == "Diciembre") {
	$('[name=mes]').val(12);	
}

document.getElementById("exportar").value = "False";
$('[name=ano]').val(anoS);

function exportarEstadistica() {
	document.getElementById("exportar").value = "True";
}