from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.core.window import Window
import matplotlib.pyplot as plt
from matplotlib import colors
from kivy.clock import Clock
from kivy.app import App
import numpy as np
import time
import os


class MapView(GridLayout):
    rid = 0
    robotName = ""
    initMap = False
    last_heard = 0
    time_out_per = 5
    unit_test_indx = 0
    track_timeout = False

    def __init__(self, srvr, **kwargs):
        super().__init__(**kwargs)
        self.attach_server(srvr)
        self.input_robot_name()
        unit_Test_Flag = self.perf_unit_test()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.initMap = False

        if unit_Test_Flag:
            Clock.schedule_interval(self.unit_test, 0.5)
        Clock.schedule_interval(self.check_server, 5)
        Clock.schedule_interval(self.ping_server, 1)

    def get_unit_test_indx(self):
        return self.unit_test_indx

    def set_unit_test_indx(self, num):
        self.unit_test_indx = num

    def set_last_heard(self, num):
        self.last_heard = num

    def get_last_heard(self):
        return self.last_heard

    def set_rid(self, rid):
        self.rid = rid

    def get_rid(self):
        loc_rid = self.rid
        return loc_rid

    def get_map(self):
        mapcur = self.mapArray
        return mapcur

    def set_robot_name(self, name):
        self.robotName = name
        print("robotNameSet!")
        return

    def get_robot_name(self):
        return self.robotName

    def init_map(self, arrayNew):
        self.mapArray = arrayNew
        self.initMap = True

    def set_map(self, mapAR):
        self.track_timeout = True
        if not self.initMap:
            self.init_map(mapAR)
        old = np.array(self.get_map())
        isSame = (old == mapAR).all()
        if not isSame:
            self.mapArray = mapAR
            os.system('clear')
            print(mapAR)
            print("Robot Id:",self.get_rid())

    def input_robot_name(self):

        while True:
            robotName = str(
                input("Enter robot Name( <10 Characters )\n")).upper()
            if len(robotName) < 10:
                self.set_robot_name(robotName)
                break
            else:
                print("Name too long \n")

    def init_robot_instance(self):
        # Send init command
        exitloop = False
        while not exitloop:
            rName = self.get_robot_name()
            print("Initialising Robot")
            cmd = "$INITROBOT,{},{}\r\n".format(rName, time.time_ns())
            self.send_cmd(cmd)
            time.sleep(0.1)
            exitloop = True

    def input_navigation(self, pressedKey):
        if self.rid != 0:

            direction = str(pressedKey).upper()
            if direction in ['W', 'A', 'S', 'D', 'X']:
                nav_cmd = "$NAVREQ,{},{},{}".format(
                    self.rid, direction, time.time_ns())
                self.send_cmd(nav_cmd)

                if direction == "X":

                    self.set_rid(0)
                    # Go into listning mode
            else:
                print("invalid input")
        else:
            self.init_robot_instance()

    def send_cmd(self, cmd):
        self.server.publish_command(cmd)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.input_navigation(keycode[1])
        return True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def perf_unit_test(self):
        flag = input("Perform Unit test?: y/n \n")

        if flag.upper() == "Y":
            return True
        else:
            return False

    def ping_server(self, dt):
        if self.get_rid() != 0:
            ping_cmd = "$PINGSERVER,{}".format(self.get_rid())
            self.send_cmd(ping_cmd)
            pass

    def check_server(self, dt):
        if(self.track_timeout):
                
            diff = time.time()-self.get_last_heard()
            if diff > self.time_out_per:
                print("Server is not active \n Closing Robot Session")
                exit()

    def unit_test(self, dt):
        cmds = ["W", "D", "S", "A"]
        i = self.get_unit_test_indx()
        self.input_navigation(cmds[i])
        i = i+1
        if i > 3:
            i = 0
        self.set_unit_test_indx(i)

    def attach_server(self, obj):
        self.server = obj


class turtleApp(App):
    rid = 0

    def __init__(self, mm, **kwargs):
        super(turtleApp, self).__init__()
        self.myMap = mm

    def build(self):

        return self.myMap
