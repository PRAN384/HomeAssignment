''' Module that takes input from the user and feeds it to the robot controller'''
import os
import sys
import numpy as np
import paho.mqtt.client as mqtt
import time
import asyncio
import threading
from  libs.helpers import * 


def on_message(client, userdata, message):
    resp= str(message.payload.decode("utf-8"))
    # print(resp)

server_broker =mqtt_broker(b_address="localhost",instance_name="Robot Server",topic_listen="robot/pos",topic_write="sitl/cmd")
server_broker.client.on_message = on_message
server_broker.client.subscribe(server_broker.topic_listen, qos=0)
server_broker.client.loop_start()



def send_cmd(cmd):
    server_broker.publish_command(cmd)


def init_robot_instance():
    ## Send init command
    maxNameLen = 10
    exitloop = False
    while not exitloop :
        robotName = str(input("Enter robot Name( <10 Characters )\n")).upper()
        if len(robotName)<10:
            cmd = "$INITROBOT,{},{}\r\n".format(robotName,time.time_ns())
            send_cmd(cmd)
            exitloop=True


def input_navigation():


    direction=input("Enter A command to move bot \n")
    direction=str(direction).upper()
    if direction in ['W','A','S','D']:        
        navcmd = "$NAVREQ,{},{}".format(rid,direction)
        send_cmd(navcmd)
    else:
        print("invalid input")


init_robot_instance()

while True:
    time.sleep(1)
#     input_navigation()


## Front end 

