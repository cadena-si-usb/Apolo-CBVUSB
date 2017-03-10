sudo /etc/init.d/apache2 stop
sudo git pull
sudo chown www-data: -R *
sudo ./models/DBINSTALL.sh
sudo /etc/init.d/apache2 start
