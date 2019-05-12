import pyfirmata
from time import sleep
import serial
import classify

"""
Make connection to the arduino via USB port.
Control movements of the servo motor, based
on condtions.
Stop movements when seeing a person.
"""


class RunServos:
    def __init__(self):
        # make a connection to the usb port
        for i in range(0, 3):
            try:
                self.board = pyfirmata.Arduino('/dev/ttyUSB{}'.format(i))
            except (FileNotFoundError, serial.serialutil.SerialException):
                continue

        # start an iterator thread so
        # serial buffer doesn't overflow
        iter8 = pyfirmata.util.Iterator(self.board)
        iter8.start()

        # set up arduino pin connections
        self.base_serv = self.board.get_pin('d:8:s')
        self.base_serv.write(90)
        self.r_serv = self.board.get_pin('d:9:s')
        self.r_serv.write(90)
        self.l_serv = self.board.get_pin('d:10:s')
        self.l_serv.write(120)

        self.angles = [
            [90, 131, 1],
            [130, 89, -1],
            [90, 49, -1],
            [50, 91, 1]
        ]
        self.thread_running = False

    def rotate_right(self):
        if classify.global_prediction is "person":
            self.thread_running = False
            return 0
        for i in range(1, 5):
            if i % 2 == 0:
                eye_left = 120
                eye_rotation_right = 90
            else:
                eye_left = 50
                eye_rotation_right = 0
            self.r_serv.write(eye_rotation_right)
            self.l_serv.write(eye_left)
            sleep(0.6)
            if classify.global_prediction is "person":
                self.thread_running = False
                return 0
        return 0

    def rotate_base(self):
        times_run = 0
        while True:
            if classify.global_prediction is "person":
                self.thread_running = False
                return 0
            for i in range(*self.angles[times_run]):
                self.base_serv.write(i)
                if classify.global_prediction is "person":
                    self.thread_running = False
                    return 0
                sleep(0.4)
            times_run += 1
            if times_run == 4:
                times_run = 0
            print("angles = {}".format(i))
            self.rotate_right()
