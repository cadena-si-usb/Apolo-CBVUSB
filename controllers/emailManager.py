# -*- encoding: utf-8 -*-

####################################################################################################################################
## DESCRIPCIÓN:
####################################################################################################################################

# Modúlo con la implementación del manejador de correo electrónico para Apolo.

####################################################################################################################################
## AUTOR:
####################################################################################################################################

# Carlos Serrada - Pyrony

####################################################################################################################################
## MODÚLOS:
####################################################################################################################################

# Libreria para facilitar el envio de correos electrónicos
from smtplib import SMTP, SMTP_SSL, SMTPAuthenticationError as AuthenticationError

# Libreria para identificar errores con la conexión a internet
from socket import gaierror as NetworkError

####################################################################################################################################
## CONSTANTES:
####################################################################################################################################

# Correo electrónico por defecto
defaultEmail = "apolo.cbvusb@gmail.com" # Dirección
defaultPass = "0800responsable"         # Contraseña

# Servidores
googleServer = "smtp.gmail.com"
yahooServer = "smtp.mail.yahoo.com"
outlookServer = "smtp.live.com"

# Puerto
tlsPort = "587" # Modo sin encryptación.. se usará por defecto
sslPort = "465" # Para usar el modo de encryptación ssl hay que comprar el certificado ssl,pero hay patria... :(

# Ruta de los templates
templatesPath = "templates/"

####################################################################################################################################
## MANEJADOR DE CORREO ELECTRÓNICO:
####################################################################################################################################

class emailManager():
    def __init__(self, server=googleServer, mail=defaultEmail, password=defaultPass):

        #---------------------------------------------------------------------------------------------------------------------------
        # Atributos:
        #---------------------------------------------------------------------------------------------------------------------------

        # Campos del correo
        self.fromMail = "Apolo <" + mail + ">"
        self.firm = self.getFirm()

        # Datos del remitente
        self.serverDir = server
        self.usermail = mail
        self.password = password

    #-------------------------------------------------------------------------------------------------------------------------------
    # Procedimientos de la clase (Métodos)
    #-------------------------------------------------------------------------------------------------------------------------------

    # Cargar plantilla para el contenido del correo
    def getTemplate(self, number):
        try:
            file = open(templatesPath+"template"+str(number)+".txt", encoding = 'utf-8', mode = "r")
            lines, template = file.read(), ""
            for line in lines: template += line.split("\n")[0]
            file.close()
            return template

        except IOError: print("ERROR: NO se encontró el archivo: template"+ str(number) + ".txt")
        except: print("Ha ocurrido un error desconocido al intentar leer el archivo: template"+ str(number) + ".txt")

    # Cargar firma
    def getFirm(self):
        try:
            file = open(templatesPath+"firm.txt", encoding = 'utf-8', mode = "r")
            lines, firm = file.read(), ""
            for line in lines: firm += line.split("\n")[0]
            file.close()
            return firm

        except IOError: print("ERROR: NO se encontró el archivo: firm.txt")
        except: print("Ha ocurrido un error desconocido al intentar leer el archivo: firm.txt")

    # Métodos para enviar correos
    def sendMail(self, toMail, toSend, sslMode = False):
        try:
            # Conectar con el servidor
            if sslMode: server = SMTP_SSL(self.serverDir + ":" + sslPort)
            else:
                server = SMTP(self.serverDir + ":" + tlsPort)
                server.starttls()

            # Iniciar sesión en el servidor
            server.login(self.usermail, self.password)

            # Mandar el correo
            server.sendmail(self.fromMail, toMail, toSend.encode("utf-8"))

            # Salir del servidor
            server.quit()

        except AuthenticationError: print("ERROR: No se pudo iniciar sesión en el servidor.")
        except NetworkError: print("ERROR: No se pudo conectar con el servidor.")
        except: print("ERROR: No se pudo enviar el correo.")

    # Método para enviar correo de recuperación de contraseña o PRM (Password Recovery Mail)
    def sendPRM(self, toMail, password):
        emailForm = "From: %s\nTo: %s\nSubject: %s\n%s\n\nContraseña: %s\n\n%s\n"          # Forma del correo
        subject = "Apolo - Reenvio de contraseña"                                          # Asunto
        template = self.getTemplate(0)                                                     # Mensaje
        toSend = emailForm%(self.fromMail, toMail, subject, template, password, self.firm) # Construir correo
        self.sendMail(toMail, toSend)                                                      # Enviar correo

####################################################################################################################################
## FIN :)
####################################################################################################################################