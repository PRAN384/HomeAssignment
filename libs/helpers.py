import time
import paho.mqtt.client as mqtt
import numpy as np
from random import randrange
import threading
class mqtt_broker:
    last_published=0
    def __init__(self,b_address,instance_name,topic_listen,topic_write):
        self.topic_listen = topic_listen
        self.topic_write = topic_write
        self.broker_address=b_address
        print("creating new instance")
        self.client = mqtt.Client(instance_name) 
        print("connecting to broker")
        self.client.connect(self.broker_address)


    def publish_command(self,command):
        self.client.publish(self.topic_write,command)
        self.last_published=time.time()


class robot():
    id =0
    curLoc=[0,0]
    tarLoc=[0,0]
    isMoving=False
    def __init__(self,name,timeStamp):
        self.name = name
        self.joined = timeStamp

    def getCurLoc(self):
        loc =self.curLoc 
        return loc

    def setCurLoc(self,newLoc):
        self.curLoc=newLoc 

    def getTarLoc(self):
        loc =self.tarLoc 
        return loc
        
    def setTarLoc(self,newLoc):
        self.tarLoc= newLoc

    def calcTarget(self,navCmd):
        curpos = self.getCurLoc()
        tarpos=[0,0]
        # print("A :Cur:{} \n Tar:{}\n".format(self.getCurLoc(),self.getTarLoc()))

        if navCmd =="W":
            tarpos[0] = curpos[0]-1
            tarpos[1] = curpos[1]
        if navCmd =="S":
            tarpos[0] = curpos[0]+1
            tarpos[1] = curpos[1]
        if navCmd =="A":
            tarpos[1] = curpos[1]-1
            tarpos[0] = curpos[0]
        if navCmd =="D":
            tarpos[1] = curpos[1]+1
            tarpos[0] = curpos[0]

        self.setTarLoc(tarpos)

    def setMoving(self,flag):
        self.isMoving = flag

    def getMoving(self):
        movingFlag= self.isMoving
        return(movingFlag)
    
class sitl_map():
    robotList = {}
    idList = []
    command_queue =[]

    def __init__(self):
        self.mapSize = self.inputMapSize()
        self.mapArray = np.zeros([self.mapSize,self.mapSize])

    def inputMapSize(self):
        exit =False
        while not exit:
            try:
                mapSize= int(input("Enter Map size <25\n"))
                if(mapSize>0 and mapSize<25):
                    exit=True
                    return mapSize
                else:
                    print("Invalid size")
            except ValueError:
                print("That was not a valid size.  Try again...")


    def AddRobot(self,obj):
        newid = self.pickID()
        self.idList.append(newid)
        obj.id = newid
        spawnPos = self.getSpawnTilePos()
        print("Spawning Robot {} at {}".format(obj.name, spawnPos))
        obj.curLoc = spawnPos
        obj.tarLoc = spawnPos
        tar_x,tar_y=obj.tarLoc
        cur_x,cur_y=obj.curLoc
        self.mapArray[tar_x,tar_y]=obj.id
        self.mapArray[cur_x,cur_y]=obj.id
        self.robotList[obj.id]=obj  ## Associating the robot with its id for easy access
        return True,obj.id

    def pickID(self):
        print(self.idList)
        if self.idList:
            mBot  = max(self.idList)
            return mBot+1
        else:
            return 1

    def DeleteRobot(self,obj):
        print("Deleting Robot {}".format(obj.id))
        tar_x,tar_y=obj.tarLoc
        cur_x,cur_y=obj.curLoc
        self.mapArray[tar_x,tar_y]=0
        self.mapArray[cur_x,cur_y]=0
        self.idList.remove(obj.id)
        del self.robotList[obj.id]

        print(self.idList,self.robotList)

        # self.robotList.pop(obj) Need to be tested

    def processQueue(self):
        while len(self.command_queue)!=0:
            print(self.command_queue)
            firstCmd= self.command_queue[0]
            locId = int(firstCmd[0])
            print("----\n",locId,self.idList)
            if locId in self.idList:
                print("Attempting Move")
                navCmd = str(firstCmd[1])
                bot =self.robotList[locId]
                if navCmd=='X':
                    self.DeleteRobot(bot)
                    self.command_queue.pop(0) ## Danger
                else:
                        
                    bot.calcTarget(navCmd)
                    ## MoveRobot
                    self.MoveRobot(bot)
                    self.command_queue.pop(0) ## Danger



    def getMap(self):
        tmpMap = self.mapArray
        return tmpMap

    def setMap(self):
        # tmpMap = 
        pass

        
    def MoveRobot(self,obj):

        tar_x,tar_y=obj.getTarLoc()
        cur_x,cur_y=obj.getCurLoc()

        withinBoundary = tar_x<self.mapSize and  tar_x>-1 and tar_y<self.mapSize and  tar_y>-1
        ## Sanity Check, are we on the boundary?
        if withinBoundary and not obj.getMoving():
            tileIsEmpty    = self.mapArray[tar_x,tar_y]==0
            if tileIsEmpty:
                obj.setMoving(True)
                self.mapArray[tar_x,tar_y]=obj.id
                self.mapArray[cur_x,cur_y]=-obj.id
                obj.setCurLoc([tar_x,tar_y])
                
                print(self.mapArray)
                
                self.Thread = threading.Timer(0.2,function=self.clearHold,args =(obj,))
                self.Thread.start()

            else:
                print("Cant! Tile isnt empty")
            
        else:
            print("On the edge")

    def getSpawnTilePos(self):
        emptyTiles = np.argwhere(self.mapArray==0)
        i = randrange(len(emptyTiles))
        return list((emptyTiles[i]))

    def cleanArray(self):
        self.mapArray[self.mapArray < 0] =0

    def clearHold(self,obj):
        self.mapArray[self.mapArray ==-obj.id]=0    
        obj.setMoving(False)
        print(self.mapArray)
        # Replace -ve nums with 0