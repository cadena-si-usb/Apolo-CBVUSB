sudo -u www-data python -c "from gluon.main import save_password; save_password(raw_input('admin password: '),443)"
sudo /etc/init.d/apache2 restart
