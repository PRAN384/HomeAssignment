import paho.mqtt.client as mqtt
from random import randrange
import numpy as np
import threading
import time
import os


class mqtt_broker:
    last_published = 0

    def __init__(self, b_address, instance_name, topic_listen, topic_write):
        self.topic_listen = topic_listen
        self.topic_write = topic_write
        self.broker_address = b_address
        print("creating new instance")
        self.client = mqtt.Client(instance_name)
        print("connecting to broker")
        self.client.connect(self.broker_address)

    def publish_command(self, command):
        self.client.publish(self.topic_write, command)
        self.last_published = time.time()


class robot():
    id = 0
    cur_loc = [0, 0]
    tar_loc = [0, 0]
    is_moving = False

    def __init__(self, name, timeStamp):
        self.name = name
        self.joined = timeStamp

    def get_cur_loc(self):
        loc = self.cur_loc
        return loc

    def set_cur_loc(self, newLoc):
        self.cur_loc = newLoc

    def get_tar_loc(self):
        loc = self.tar_loc
        return loc

    def set_tar_loc(self, newLoc):
        self.tar_loc = newLoc

    def set_moving_flag(self, flag):
        self.is_moving = flag

    def get_moving_flag(self):
        flag = self.is_moving
        return (flag)

    def calc_tar(self, nav_cmd):
        cur_pos = self.get_cur_loc()
        tar_pos = [0, 0]
        if nav_cmd == "W":
            tar_pos[0] = cur_pos[0]-1
            tar_pos[1] = cur_pos[1]
        if nav_cmd == "S":
            tar_pos[0] = cur_pos[0]+1
            tar_pos[1] = cur_pos[1]
        if nav_cmd == "A":
            tar_pos[1] = cur_pos[1]-1
            tar_pos[0] = cur_pos[0]
        if nav_cmd == "D":
            tar_pos[1] = cur_pos[1]+1
            tar_pos[0] = cur_pos[0]

        self.set_tar_loc(tar_pos)


class sitl_map():
    robot_list = {}
    robot_ping = {}
    id_list = []
    command_queue = []
    time_out_per = 5

    def __init__(self):
        self.mapSize = self.input_map_size()
        self.map_array = np.zeros([self.mapSize, self.mapSize])
        check_robtos = threading.Thread(
            target=self.check_server, name="check_active_robots", args=())
        check_robtos.start()

    def input_map_size(self):
        exit = False
        while not exit:
            try:
                mapSize = int(input("Enter Map size <25\n"))
                if (mapSize > 0 and mapSize < 25):
                    exit = True
                    return mapSize
                else:
                    print("Invalid size")
            except ValueError:
                print("That was not a valid size.  Try again...")

    def add_robot(self, obj):
        newid = self.pick_id()
        if newid != 0:
            self.id_list.append(newid)
            obj.id = newid
            spawnpos = self.get_spawn_tile()
            if type(spawnpos) != int:
                print("Spawning Robot {} at {}".format(obj.name, spawnpos))
                obj.cur_loc = spawnpos
                obj.tar_loc = spawnpos
                tar_x, tar_y = obj.tar_loc
                cur_x, cur_y = obj.cur_loc
                self.map_array[tar_x, tar_y] = obj.id
                self.map_array[cur_x, cur_y] = obj.id
                # Associating the robot with its id for easy access
                self.robot_list[obj.id] = obj
                return True, obj.id
            else:
                return False, 0
        else:
            pass

    def get_spawn_tile(self):
        empty_tiles = np.argwhere(self.map_array == 0)
        if len(empty_tiles) != 0:

            i = randrange(len(empty_tiles))
            return list((empty_tiles[i]))
        else:
            return 0  # Cant add

    def pick_id(self):
        if self.id_list:
            mBot = max(self.id_list)
            return mBot+1
        else:
            return 1

    def delete_robot(self, obj):
        print("Deleting Robot {}".format(obj.id))
        tar_x, tar_y = obj.tar_loc
        cur_x, cur_y = obj.cur_loc
        self.map_array[tar_x, tar_y] = 0
        self.map_array[cur_x, cur_y] = 0
        self.id_list.remove(obj.id)
        del self.robot_list[obj.id]
        del self.robot_ping[obj.id]
        # print(self.id_list, self.robot_list)
        # self.robot_list.pop(obj) Need to be tested

    def process_queue(self):
        while len(self.command_queue) != 0:
            # print(self.command_queue)
            firstCmd = self.command_queue[0]
            id = int(firstCmd[0])
            if id in self.id_list:
                nav_cmd = str(firstCmd[1])
                bot = self.robot_list[id]
                if nav_cmd == 'X':
                    self.delete_robot(bot)
                    self.command_queue.pop(0)
                else:
                    bot.calc_tar(nav_cmd)
                    self.move_robot(bot)
                    self.command_queue.pop(0)

    def get_robot_list(self):
        updateDict = {}
        robot_dict = self.robot_list
        for i in robot_dict.keys():
            r = robot_dict[i]
            updateDict[i] = [r.name, r.get_cur_loc()]
        return updateDict

    def get_map(self):
        tmpMap = self.map_array
        return tmpMap

    def move_robot(self, obj):
        tar_x, tar_y = obj.get_tar_loc()
        cur_x, cur_y = obj.get_cur_loc()

        within_bounds = tar_x < self.mapSize and tar_x > - \
            1 and tar_y < self.mapSize and tar_y > -1
        # Sanity Check, are we on the boundary?
        if within_bounds and not obj.get_moving_flag():
            tile_is_empty = self.map_array[tar_x, tar_y] == 0
            if tile_is_empty:
                obj.set_moving_flag(True)
                self.map_array[tar_x, tar_y] = obj.id
                self.map_array[cur_x, cur_y] = -obj.id
                obj.set_cur_loc([tar_x, tar_y])

                # print(self.map_array)

                self.Thread = threading.Timer(
                    0.2, function=self.clear_hold, args=(obj,))
                self.Thread.start()

            else:
                pass

        else:
            pass

    def clear_hold(self, obj):
        os.system('clear')
        print(self.map_array)
        self.map_array[self.map_array == -obj.id] = 0
        obj.set_moving_flag(False)
        # Replace -ve nums with 0

    def update_robot_ping(self, id):
        self.robot_ping[id] = time.time()

    def check_server(self):
        while True:
            for k in self.robot_ping.keys():
                if (time.time()-self.robot_ping[k]) > self.time_out_per:
                    bot = self.robot_list[k]
                    print("Deleting Robot")
                    self.delete_robot(bot)
                    break
                else:
                    pass
            time.sleep(5)
