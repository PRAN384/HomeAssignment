import time
import paho.mqtt.client as mqtt
import numpy as np
from random import randrange
class mqtt_broker:
    last_published=0
    def __init__(self,b_address,instance_name,topic_listen,topic_write):
        self.topic_listen = topic_listen
        self.topic_write = topic_write
        self.broker_address=b_address#"192.168.183.240"
        #broker_address="iot.eclipse.org"
        print("creating new instance")
        self.client = mqtt.Client(instance_name) #create new instance
        # self.client.on_message=self.on_message #attach function to callback
        print("connecting to broker")
        self.client.connect(self.broker_address) #connect to broker    

    # def on_message(self,client, userdata, message):
    #     print("message received " ,str(message.payload.decode("utf-8")))
    #     print("message topic=",message.topic)
    #     print("message qos=",message.qos)
    #     print("message retain flag=",message.retain)

    def publish_command(self,command):
        self.client.publish(self.topic_write,command)
        self.last_published=time.time()
        print("Command sent to cs")

class robot():
    id =0
    curLoc=[0,0]
    tarLoc=[0,0]
    def __init__(self,name,timeStamp):
        self.name = name
        self.joined = timeStamp


class sitl_map():
    robotList = []
    command_queue =[]
    emptyTiles =[]
    ids=[]

    def __init__(self,mapsize):
        self.mapSize = mapsize
        self.mapArray = np.zeros([self.mapSize,self.mapSize])

    def AddRobot(self,obj):
        newid = len(self.ids)+1
        obj.id = newid
        spawnPos = self.getSpawnTilePos()
        print("Spawning Robot {} at {}".format(obj.name, spawnPos))
        obj.curLoc = spawnPos
        obj.tarLoc = spawnPos
        tar_x,tar_y=obj.tarLoc
        cur_x,cur_y=obj.curLoc
        self.mapArray[tar_x,tar_y]=1
        self.mapArray[cur_x,cur_y]=1
        self.robotList.append(obj)


    def DeleteRobot(self,obj):
        tar_x,tar_y=obj.tarLoc
        cur_x,cur_y=obj.curLoc
        self.mapArray[tar_x,tar_y]=0
        self.mapArray[cur_x,cur_y]=0
        self.robotList.pop(obj)

   
    def MoveRobot(self,obj):
        
        tar_x,tar_y=obj.tarLoc
        cur_x,cur_y=obj.curLoc

        if self.mapArray[tar_x,tar_y]==0: 
            self.mapArray[tar_x,tar_y]=1
            self.mapArray[cur_x,cur_y]=-1
        else:
            print()
            pass    
        ## Move and update empty tiles

    def getSpawnTilePos(self):
        randomNums= np.arange(1,self.mapSize+1)
        finish=False
        emptyTiles = np.argwhere(self.mapArray==0)
        i = randrange(len(emptyTiles))
        return list((emptyTiles[i]))


        
