import asyncio
import time
import numpy as np
import paho.mqtt.client as mqtt
from  libs.helpers import *
import json


SITL = sitl_map()

def on_message(client, userdata, message):
    req= str(message.payload.decode("utf-8"))
    header= req.split(',')[0]
    if header =="$INITROBOT":
        rName = req.split(',')[1]
        initTime = req.split(',')[2]
        success,id= SITL.AddRobot(robot(rName,initTime))

        if success:
            print("Sending Init success")
            client_broker.publish_command("$INITROBOTS,{},{}".format(rName,id))

    if header =="$NAVREQ":
        print("Got command")
        id      =    req.split(',')[1]
        dir     =    req.split(',')[2]
        cmdTime =    req.split(',')[3]
        command = [id,dir,cmdTime]
        SITL.command_queue.append(command)



client_broker = mqtt_broker(b_address="localhost",\
                            instance_name="SITL Server",\
                            topic_listen="sitl/cmd",\
                            topic_write="robot/pos")
client_broker.client.on_message = on_message
client_broker.client.subscribe(client_broker.topic_listen, qos=0)
client_broker.client.loop_start()

def broadcastMap():
    while True:
        listMap = SITL.getMap().tolist()
        encMap = json.dumps(listMap)
        client_broker.publish_command("$NAVBROAD,:{}:{}".format(encMap,time.time_ns()))
        time.sleep(0.1)

PosBroadCastThread= threading.Thread(target=broadcastMap,name="Position BroadCast",args=())
PosBroadCastThread.start()

while True:    
    SITL.processQueue()