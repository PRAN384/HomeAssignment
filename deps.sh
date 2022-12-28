#!/bin/bash


## Mosquitto Server installation and running 
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
sudo apt clean
pip3 install paho-mqtt
## Need Testing 






















