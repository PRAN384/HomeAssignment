from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App
import numpy as np
import kivy
from kivy.properties import ListProperty


class MapView(GridLayout):
    mapArray = []

    mapsize=10
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols= self.mapsize
        for i in np.arange(0,self.mapsize):
            for j in np.arange(0,self.mapsize):
                self.add_widget(customButton(text="".format(i,j),id="{}_{}".format(i,j),on_press=self.pressed))


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