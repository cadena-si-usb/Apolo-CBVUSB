#! /bin/bash
sudo apt-get -y install python-psycopg2 postgresql
sudo rm -v -f databases/*
sudo -u postgres dropdb cbvusb
sudo -u postgres dropuser cbvusb
sudo -u postgres createuser -PE -s cbvusb
sudo -u postgres createdb -O cbvusb -E UTF8 cbvusb
