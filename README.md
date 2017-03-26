# [Apolo](http://apolo.bomberos.usb.ve "Ir a apolo")
*Sistema de gestión para el Cuerpo de Bomberos Voluntarios de la Universidad Simón Bolívar (CBVUSB)*

## Autores

1. Pyrony:
   + Carlos Serrada
   + Mathias San Miguel
   + Augusto Hidalgo
   + Rubmary Rojas
   + José Acevedo
   + Juan Ortiz
   + Pablo Betancourt
   + Jonathan Reyes
   + Irina Marcano

2. NOS (Number One Software):
   + Christian Oliveros
   + Alexander Romero
   + Lalezka Duque
   + Marcos Jota
   + Daniel Valera
   + Carlos Infante
   + Midaysa Palacios
   + Génesis Kufatty
   + Salvador Covelo

## Estado del proyecto
30% del sistema completado. Algunas de las funcionalidades del sistema son:
   + Registro de servicio
   + Guardar borrador de servicio
   + Editar servicio
   + Listar servicios
   + Ver detalles de servicio
   + Aprobar servicio
   + Iniciar sesión
   + Registrar usuario
   + Modificar perfil
   + Ver perfil
   + Ver estadísticas públicas
   + Exportar servicio
   + Exportar estadísticas
   + Enviar constancias
   + Notificaciones de actividad por correo electrónico

## Errores conocidos
   + La función de envio de constancia no funciona en el servidor
   + Al eliminar alguna instancia de un multivaluado en el formulario de registro de servicio, no se actualiza el contador para las instancias que venian despues de la eliminada.

## Especificaciones técnicas
1. Requeirmientos del sistema
   + PostgreSQL 9.X
   + Python v2.7.x
   + Libreria python-ldap
   + Libreia psycopg2
   + wkhtmltopdf

2. Versiones de los componentes
   + Bootstrap v3.3.5             (incluido)
   + Bootstrap datePicker v1.7.0  (incluido)
   + Jquery v3.1.1                (incluido)
   + Jquery dataTables v1.10.13   (incluido)
   + Jquery datePair v0.4.15      (incluido)
   + Jquery formValidator v2.3.55 (incluido)
   + Jquery timePicker v1.11.10   (incluido)
   + SweetAlert                   (incluido)

## Instalación:

+ Descargar web2py. Puede hacerlo haciendo click [aquí](http://www.web2py.com/init/default/download "Descargar web2py").
+ Extraer la carpeta contenida en el comprimido de web2py en su home.
+ Abrir un terminal.
+ Clonar el repositorio.
```bash
git clone https://github.com/cadena-si-usb/Apolo-CBVUSB apolo
```
+ Mover la carpeta "apolo" en "web2py/applications/".
```bash
mv apolo web2py/applications/
```
+ Ir a "web2py/applications/apolo/" y ejecutar el script de instalación.
```bash
cd web2py/applications/apolo/
sudo ./DBINSTALL.sh
```
+ Ingresar "1234" cuando solicite la contraseña para crear el nuevo role