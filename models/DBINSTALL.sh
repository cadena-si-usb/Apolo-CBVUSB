#! /bin/bash
sudo apt-get -y install python-psycopg2
#read -s -p "Por favor ingrese su contraseña para la base de datos de postgres: "  password
#echo "ALTER USER postgres WITH PASSWORD '$password';" > first.sql
#psql postgres -f first.sql
rm ~/.psql_history 2> /dev/null
sudo -u postgres createuser -PE -s cbvusb
sudo -u postgres createdb -O cbvusb -E UTF8 cbvusb
#read -s -p "Por favor ingrese su contraseña para la base de datos del sistema Apolo: " password
#echo "ALTER USER cvusb WITH PASSWORD '$password';" > first.sql
#psql cbvusb -f first.sql
rm ~/.psql_history 2> /dev/null
#rm first.sql
