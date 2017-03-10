sudo /etc/init.d/apache2 stop
sudo chown root: -R *
sudo git pull
sudo chown www-data: -R *
sudo ./models/DBINSTALL.sh
sudo /etc/init.d/apache2 start
