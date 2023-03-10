import numpy as np
import paho.mqtt.client as mqtt
import time
from libs.helpers import *
from libs.guilib import *
import json
import threading

server_broker = mqtt_broker(b_address="localhost", instance_name="Robot client{}".format(
    time.time_ns()), topic_listen="robot/pos", topic_write="sitl/cmd")
mm = MapView(server_broker)
mm.attach_server(server_broker)
frontEnd = turtleApp(mm)

def on_message(client, userdata, message):
    rep = str(message.payload.decode("utf-8"))
    header = rep.split(',')[0]
    if header == "$INITROBOTS":
        if frontEnd.myMap.get_rid() == 0:
            name = rep.split(',')[1]
            if name == frontEnd.myMap.get_robot_name():
                rid = int(rep.split(',')[2])
                if rid != 0:
                    frontEnd.myMap.set_rid(rid)
                else:
                    print("Grid is Full")

    if header == "$NAVBROAD":  # and frontEnd.myMap.getRID()!=0:
        __, jsonData = rep.split(":")
        mapList = json.loads(jsonData)
        mapAr = np.array(mapList)
        frontEnd.myMap.set_map(mapAr)
        frontEnd.myMap.set_last_heard(time.time())

server_broker.client.on_message = on_message
server_broker.client.subscribe(server_broker.topic_listen, qos=0)
meassgeThread = threading.Thread(
    target=server_broker.client.loop_start, name="msg", args=())
meassgeThread.start()

frontEnd.run()
