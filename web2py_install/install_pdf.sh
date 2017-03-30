sudo apt-get -y install libxrender1 xfonts-utils xfonts-base xfonts-75dpi libfontenc1 x11-common xfonts-encodings libxfont1 fontconfig
wget https://downloads.wkhtmltopdf.org/0.12/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar xf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
cd wkhtmltox/bin/
sudo mv wkhtmltopdf /usr/bin/wkhtmltopdf
cd ../..
