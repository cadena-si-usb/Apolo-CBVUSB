#[Apolo](apolo.bomberos.usb.ve "Ir a apolo")
*Sistema de gestión para el Cuerpo de Bomberos Voluntarios de la Universidad Simón Bolívar (CBVUSB)*

##Autores

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

##Estado del proyecto
20% del sistema completado.

##Especificaciones técnicas
1. Requeirmientos del sistema
   + Python v2.7.x

2. Versiones de los componentes
   + Bootstrap v3.3.5             (incluido)
   + Bootstrap datePicker v1.7.0  (incluido)
   + Jquery v3.1.1                (incluido)
   + Jquery dataTables v1.10.13   (incluido)
   + Jquery datePair v0.4.15      (incluido)
   + Jquery formValidator v2.3.55 (incluido)
   + Jquery timePicker v1.11.10   (incluido)
   + Jquery UI v1.12.1            (incluido)
   + SweetAlert                   (incluido)

##Instalación:

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
