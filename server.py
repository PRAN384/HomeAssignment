import asyncio
import time
import numpy as np
import paho.mqtt.client as mqtt
# class WebServer:
#     def __init__(self, **kwargs: dict):
#         self.app = web.Application()
#         self.host = kwargs['webserver']['host']
#         self.port = kwargs['webserver']['port']
#         self.dbConf = kwargs['db']
#         self.dbEngine = None
#         self.sessionToUser = {}
#         self.userToSession = {}


class mqtt_broker:
    def __init__(self,b_address,instance_name,topic):
        self.topic = topic
        self.broker_address=b_address#"192.168.183.240"
        #broker_address="iot.eclipse.org"
        print("creating new instance")
        self.client = mqtt.Client(instance_name) #create new instance
        self.client.on_message=self.on_message #attach function to callback
        print("connecting to broker")
        self.client.connect(self.broker_address) #connect to broker    

    def on_message(self,client, userdata, message):
        pass

    def publish_command(self,command):
        if (time.time()-self.last_published > .01):
            self.client.publish(self.topic,command)
            self.last_published=time.time()
            print("Command sent to cs")
            
            
server_broker = mqtt_broker("192.168.1.71","SITL Server","robot/pos")

server_broker.client.loop_start()

server_broker.publish_command("yellow!")



