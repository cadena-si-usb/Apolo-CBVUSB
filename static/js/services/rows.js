$(document).ready(function() {
    // Función para hacer clickeables las filas de las tablas y redirigir al href correspondiente
    $("body").on("click", ".clickable-row", function() {
        window.location = $(this).data("href");
    });
});