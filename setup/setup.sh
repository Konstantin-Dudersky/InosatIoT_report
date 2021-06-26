#!/bin/bash

echo
echo "-----> Updating system:"
sudo apt update
sudo apt -y upgrade

echo
echo "-----> Python version:"
python3 -V

echo
echo "-----> Install python base packages:"
sudo apt install -y python3-pip
sudo apt install -y python3-venv

echo
echo "-----> Create virtual environment:"
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r setup/requirements.txt

echo
echo "-----> Create systemd service"
python3 setup/inosatiot_report.py
sudo cp setup/inosatiot_report.service /etc/systemd/system
rm setup/inosatiot_report.service
sudo systemctl daemon-reload
sudo systemctl enable inosatiot_report.service