''' Module that takes input from the user and feeds it to the robot controller'''
import os
import sys
import numpy as np
import paho.mqtt.client as mqtt
import time
from  libs.helpers import * 
import json

from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App
import numpy as np
import kivy
from kivy.properties import ListProperty



robotName = str(input("Enter robot Name( <10 Characters )\n")).upper()

def on_message(client, userdata, message):
    rep= str(message.payload.decode("utf-8"))
    header= rep.split(',')[0]
    if header =="$INITROBOTS":
        if  rid==0 :
            name = rep.split(',')[1]
            if name==robotName:
                rid = int(rep.split(',')[2])
                TestApp.myMap.setRID(rid)

    if header =="$NAVBROAD":
        __,jsonData,updated = rep.split(":")
        mapList = json.loads(jsonData)
        mapAr = np.array(mapList)
        # localMap.set

server_broker =mqtt_broker(b_address="localhost",instance_name="Robot Server_{}".format(time.time_ns()),topic_listen="robot/pos",topic_write="sitl/cmd")
server_broker.client.on_message = on_message
server_broker.client.subscribe(server_broker.topic_listen, qos=0)
server_broker.client.loop_start()

def send_cmd(cmd):
    server_broker.publish_command(cmd)

def init_robot_instance():
    ## Send init command
    maxNameLen = 10
    exitloop = False
    while not exitloop :
        if len(robotName)<10:
            print("Initialising Robot")
            cmd = "$INITROBOT,{},{}\r\n".format(robotName,time.time_ns())
            send_cmd(cmd)
            time.sleep(0.1)
            exitloop=True

class MapView(GridLayout):
    mapArray = []
    rid=0
    mapsize=10
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols= self.mapsize
        for i in np.arange(0,self.mapsize):
            for j in np.arange(0,self.mapsize):
                self.add_widget(customButton(text="".format(i,j),id="{}_{}".format(i,j),on_press=self.pressed))
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_interval(self.updateGrid,0.1)    

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    def input_navigation(self,pressedKey):
        if self.rid != 0:

            direction=str(pressedKey).upper()
            if direction in ['W','A','S','D']:        
                navcmd = "$NAVREQ,{},{},{}".format(self.rid,direction,time.time_ns())
                send_cmd(navcmd)
            else:
                print("invalid input")
        else:
            init_robot_instance()    

    def setRID(self,ID):
        self.rid = ID

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        self.input_navigation(keycode[1])
        return True

    def pressed(self,mybutton):
        print(mybutton.id)

    def updateGrid(self,dt):
        pass
        # print("Calling")
        # self.mapArray = array

class customButton(Button):
    def __init__(self,id, **kwargs,):
        super().__init__(**kwargs)
        self.id = id
        self.border = [21, 21, 21, 21]


class TestApp(App):
    def build(self):
        self.myMap =MapView() 
        Clock.schedule_interval(self.myMap.updateGrid,0.1)
        return self.myMap

    def setMap(self,array):
        self.myMap.mapArray =array

TestApp().run()












