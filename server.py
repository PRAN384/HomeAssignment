import asyncio
import time
import numpy as np
import paho.mqtt.client as mqtt
from  libs.helpers import *


MAP = sitl_map(5)

def on_message(client, userdata, message):
    req= str(message.payload.decode("utf-8"))
    ## Message types and actions associated to each
    ## Init bot
    header= req.split(',')[0]
    if header =="$INITROBOT":
    # <1>: Robot ID
        rName = req.split(',')[1]
        initTime = req.split(',')[2]
        success,id= MAP.AddRobot(robot(rName,initTime))
        if success:
            print("Sending Init success")
            client_broker.publish_command("$INITROBOTS,{},{}".format(rName,id))

    if header =="$NAVREQ":
        id      =    req.split(',')[1]
        dir     =    req.split(',')[2]
        cmdTime =    req.split(',')[3]
        command = [id,dir,cmdTime]
        MAP.command_queue.append(command)
        # print(MAP.command_queue)

client_broker = mqtt_broker(b_address="localhost",\
                            instance_name="SITL Server",\
                            topic_listen="sitl/cmd",\
                            topic_write="robot/pos")
client_broker.client.on_message = on_message
client_broker.client.subscribe(client_broker.topic_listen, qos=0)
client_broker.client.loop_start()

t= 0
dt = 0.01

def sendMap():
    client_broker.publish_command("$NAVBROAD,{},{}".format(MAP.mapArray,time.time_ns))

    pass

while t>-1:
    # print(MAP.mapArray)    
    # MAP.cleanArray()
    MAP.processQueue()
    t+=dt