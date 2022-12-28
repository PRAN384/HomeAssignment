import time
from libs.helpers import *
import json


SITL = sitl_map()


def on_message(client, userdata, message):
    req = str(message.payload.decode("utf-8"))
    header = req.split(',')[0]
    if header == "$INITROBOT":  # initial
        rName = req.split(',')[1]
        initTime = req.split(',')[2]
        success, id = SITL.add_robot(robot(rName, initTime))

        if success:
            print("Sending Init success")
        else:
            print("Grid is Full")

        client_broker.publish_command(
            "$INITROBOTS,{},{}".format(rName, id))

    if header == "$NAVREQ":
        id = req.split(',')[1]
        dir = req.split(',')[2]
        cmdTime = req.split(',')[3]
        command = [id, dir, cmdTime]
        SITL.command_queue.append(command)

    if header == "$PINGSERVER":
        id = int(req.split(',')[1])
        SITL.update_robot_ping(id)


client_broker = mqtt_broker(b_address="localhost",
                            instance_name="SITL Server",
                            topic_listen="sitl/cmd",
                            topic_write="robot/pos")
client_broker.client.on_message = on_message
client_broker.client.subscribe(client_broker.topic_listen, qos=0)
client_broker.client.loop_start()


def broadcast_map():
    while True:
        listMap = SITL.get_map().tolist()
        encMap = json.dumps(listMap)
        client_broker.publish_command(
            "$NAVBROAD,:{}".format(encMap))
        time.sleep(0.1)


PosBroadCastThread = threading.Thread(
    target=broadcast_map, name="Position Broadcast", args=())
PosBroadCastThread.start()

while True:

    SITL.process_queue()
