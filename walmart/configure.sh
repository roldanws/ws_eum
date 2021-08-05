#sudo apt-get install python3-pip
pip install -r req.txt



echo hay va
sudo rm -r /usr/share/eum
sudo cp -r ../eum/ /usr/share/
sudo rm /usr/local/share/applications/inicio.desktop
sudo cp inicio.desktop /usr/share/applications/

#sudo cp vista.service /lib/systemd/system/
#sudo systemctl daemon-reload
#sudo systemctl enable vista.service
#sudo systemctl start vista.service
#sudo systemctl status vista.service
pwd
echo hay fue


read -p 'Numero de equipo: ' numero
python manage.py createsuperuser
