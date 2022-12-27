''' Module that takes input from the user and feeds it to the robot controller'''
import os
import sys
import numpy as np
import paho.mqtt.client as mqtt
import time
from  libs.helpers import * 
from  libs.guilib import * 
import json
import threading

# mm.setRobotName(robotName)
server_broker =mqtt_broker(b_address="localhost",instance_name="Robot Server_{}".format(time.time_ns()),topic_listen="robot/pos",topic_write="sitl/cmd")
mm  = MapView(server_broker)
mm.attachServer(server_broker)
frontEnd = TestApp(mm)

def print_fun(msg):
    print(msg)
    print("\n\n\n\n\n\n")



def on_message(client, userdata, message):
    rep= str(message.payload.decode("utf-8"))
    header= rep.split(',')[0]
    if header =="$INITROBOTS":
        if  frontEnd.myMap.getRID()==0 :
            name = rep.split(',')[1]
            if name==frontEnd.myMap.getRobotName():
                rid = int(rep.split(',')[2])
                frontEnd.myMap.setRID(rid)

    if header =="$NAVBROAD":
        __,jsonData,updated = rep.split(":")
        mapList = json.loads(jsonData)
        mapAr = np.array(mapList)
        frontEnd.myMap.setMap(mapAr)


server_broker.client.on_message = on_message
server_broker.client.subscribe(server_broker.topic_listen, qos=0)
# msgThrd = server_broker.client.loop_start()

meassgeThread= threading.Thread(target=server_broker.client.loop_start,name="msg",args=())
meassgeThread.start()






        # localMap.set



# def send_cmd(cmd):
#     server_broker.publish_command(cmd)

# def init_robot_instance():
#     ## Send init command
#     maxNameLen = 10
#     exitloop = False
#     while not exitloop :
#         if len(robotName)<10:
#             print("Initialising Robot")
#             cmd = "$INITROBOT,{},{}\r\n".format(robotName,time.time_ns())
#             send_cmd(cmd)
#             time.sleep(0.1)
#             exitloop=True
            
# frontEnd.inti_bot = init_robot_instance(robotName)
frontEnd.run()
# TestApp().run()