import asyncio
import time
import numpy as np
import paho.mqtt.client as mqtt
from  libs.helpers import *


MAP = sitl_map(10)

def on_message(client, userdata, message):
    req= str(message.payload.decode("utf-8"))
    ## Message types and actions associated to each
    ## Init bot
    header= req.split(',')[0]
    if header =="$INITROBOT":
    # <1>: Robot ID
        rName = req.split(',')[1]
        initTime = req.split(',')[2]
        MAP.AddRobot(robot(rName,initTime))

    print(MAP.mapArray)


client_broker = mqtt_broker(b_address="localhost",\
                            instance_name="SITL Server",\
                            topic_listen="sitl/cmd",\
                            topic_write="robot/pos")
client_broker.client.on_message = on_message
client_broker.client.subscribe(client_broker.topic_listen, qos=0)
client_broker.client.loop_start()

while True:
    


    time.sleep(0.1)
    # client_broker.publish_command("yellow!")
    # print(MAP.mapArray)
