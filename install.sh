#! /bin/bash

apt-get update 
apt-get install -y unzip libcanberra-gtk-module libgconf-2-4 libatomic1 python3.7-venv
if [ ! -d "env" ]
then
    python3.7 -m venv env
    source env/bin/activate
    python3.7 -m pip install -r requirements.txt
else
    source env/bin/activate
fi

echo "Running updater..."

./env/bin/python main.py

if [ -f "/usr/bin/popcorn-time" ]
then
    echo "Setting execution permissions..."
    chmod +x /usr/bin/popcorn-time
fi