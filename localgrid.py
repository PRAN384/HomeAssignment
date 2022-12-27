## Test for creating Gui logic with updating

from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
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
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty


class mapWid(RelativeLayout):
    ids=0
    pass

    # def createGrid()









class TestApp(App):
    rid = 0
    # def __init__(self,**kwargs):
    #         super(TestApp, self).__init__()

    #         # self.myMap =MapView() 




    def build(self):
        # self.myMap =MapView() 
        # Clock.schedule_interval(self.myMap.updateGrid,0.1)
        return mapWid()




TestApp().run()