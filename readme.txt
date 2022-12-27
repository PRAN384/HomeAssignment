Installation of dependencies:

For ubuntu:

sudo ./deps.sh
pip install -r requirements.txt

For windows:

Install mosquitto server from https://mosquitto.org/download/
pip install -r requirements.txt

To run the simulation:
1. Run server.py on a machine
2. Input grid size(max size set to 25)
3. Start robotinterface.py
4. Input robot name
5. Select unit test by entering y/n
6. If y, an array will be presented in the terminal with an int value moving clockwise in a 1 X 1 square.
7. If n, click on the black "Test" window and start pressing the nav commands. The integer value on the square will start moving in the commanded direction.
   You can still command the robot using W(up),A(left),S(down),D(right) during the unit test.The square pattern will start once you stop pressing keys. The movement might be erratic.
8. Press x to stop the robot interface, and it will delete the value on the array.

