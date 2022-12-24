import time
import paho.mqtt.client as mqtt

class mqtt_broker:
    last_published=0
    def __init__(self,b_address,instance_name,topic_listen,topic_write):
        self.topic_listen = topic_listen
        self.topic_write = topic_write
        self.broker_address=b_address#"192.168.183.240"
        #broker_address="iot.eclipse.org"
        print("creating new instance")
        self.client = mqtt.Client(instance_name) #create new instance
        self.client.on_message=self.on_message #attach function to callback
        print("connecting to broker")
        self.client.connect(self.broker_address) #connect to broker    

    def on_message(self,client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)

    def publish_command(self,command):
        if (time.time()-self.last_published > .01):
            self.client.publish(self.topic_write,command)
            self.last_published=time.time()
            print("Command sent to cs")