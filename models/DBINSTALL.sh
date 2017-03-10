#! /bin/bash
sudo apt-get -y install python-psycopg2 postgresql
sudo /etc/init.d/postgresql restart
rm ~/.psql_history 2> /dev/null
rm -f ../databases/*
sudo -u postgres dropdb cbvusb
sudo -u postgres dropuser cbvusb
sudo -u postgres createuser -PE -s cbvusb
sudo -u postgres createdb -O cbvusb -E UTF8 cbvusb
rm ~/.psql_history 2> /dev/null
sudo /etc/init.d/apache2 stop
