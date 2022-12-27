from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg
# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
import matplotlib.pyplot as plt
from matplotlib import colors
from kivy.clock import Clock
from kivy.app import App
import numpy as np
import time
import os
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty


class MapView(GridLayout):
    rid=0
    robotName=""
    init_map = False
    def __init__(self,srvr, **kwargs):
        super().__init__(**kwargs)
        self.attachServer(srvr)
        self.inputRobotName()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        # Clock.schedule_interval(self.printMap,0.1)    

    def addPlt(self):
            self._added = True
            cmap = colors.ListedColormap(['Blue','red','green'])
            curMap = self.getMap()
            curMap[curMap<0]=0
            plt.figure(figsize=(6,6))
            plt.pcolor(curMap[::-1],cmap=cmap,edgecolors='k', linewidths=3)
            plt.grid(True)
            self.fig1 = plt.gcf()
            self.add_widget(FigureCanvasKivyAgg(self.fig1))
        
    def clearUpdate(self):
            cmap = colors.ListedColormap(['Blue','red','green'])
            curMap = self.getMap()
            curMap[curMap<0]=0
            plt.pcolor(curMap[::-1],cmap=cmap,edgecolors='k', linewidths=3)
            plt.grid(True)
            self.fig1 = plt.gcf()
            self.add_widget(FigureCanvasKivyAgg(self.fig1))

    def Update(self,dt):
        # if self._added:
        plt.cla()
        self.clear_widgets()
        self.addPlt()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def setRID(self,rid):
        self.rid= rid    

    def getRID(self):
        locRID = self.rid
        return locRID   

    def getMap(self):
        mapcur=self.mapArray
        return mapcur

    def initMap(self,arrayNew):               
        self.mapArray = arrayNew

    def setMap(self,mapAR):
        if not self.init_map:
            self.initMap(mapAR)
            self.init_map=True

        old= np.array(self.getMap())
        isSame = (old==mapAR).all()
        if not isSame:
            self.mapArray =mapAR
            # os.system( 'clear' )
            print(mapAR)

    def printMap(self,dt):
        print("\n\n\n\n")
        print(self.mapArray)

    def input_navigation(self,pressedKey):
        if self.rid != 0:

            direction=str(pressedKey).upper()
            if direction in ['W','A','S','D','X']:        
                navcmd = "$NAVREQ,{},{},{}".format(self.rid,direction,time.time_ns())
                self.send_cmd(navcmd)

                if direction=="X":

                    self.setRID(0)
                    ## Go into listning mode
            else:
                print("invalid input")
        else:
            self.init_robot_instance()    

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.input_navigation(keycode[1])
        return True

    def attachServer(self,obj):
        self.server = obj

    def inputRobotName(self):

        while True:
            robotName = str(input("Enter robot Name( <10 Characters )\n")).upper()
            if len(robotName)<10:
                self.setRobotName(robotName)
                break
            else:
                print("Name too long \n")

    def setRobotName(self,name):
        self.robotName= name
        print("robotNameSet!")
        return

    def getRobotName(self):
        return self.robotName

    def send_cmd(self,cmd):
        self.server.publish_command(cmd)

    def init_robot_instance(self):
        ## Send init command
        maxNameLen = 10
        exitloop = False
        while not exitloop :
            rName = self.getRobotName()
            print(rName)
            if len(rName)<10:
                print("Initialising Robot")
                cmd = "$INITROBOT,{},{}\r\n".format(rName,time.time_ns())
                self.send_cmd(cmd)
                time.sleep(0.1)
                exitloop=True

class TestApp(App):
    rid = 0
    def __init__(self, mm,**kwargs):
            super(TestApp, self).__init__()
            self.myMap = mm
            # self.myMap =MapView() 




    def build(self):
        # self.myMap =MapView() 
        # Clock.schedule_interval(self.myMap.updateGrid,0.1)
        return self.myMap



