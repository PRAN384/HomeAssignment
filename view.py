from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App
import numpy as np
import kivy
from kivy.properties import ListProperty


class MapView(RelativeLayout):
    mapArray = []
    mapsize=10
    __built = False
    grid=[]
    def __init__(self, *data, **kwargs):

        if not MapView.__built:
            MapView.__built = True
        super(MapView, self).__init__(**kwargs)
        # Put the scheduler




    def pressed(self,mybutton):
        print(mybutton.id)
        ## Create the layout
    def updateGrid(self,array):
        print("Calling")
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
    def updateApp(self,array):
        self.myMap.updateGrid(array)

TestApp().run()