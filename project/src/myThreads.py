import time
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal


# class DeviceConnect(QObject):
#     finished = pyqtSignal(bool)
#     progress = pyqtSignal(int)
#
#     def run(self):
#         DevSer = serial.Serial('COM9', 38400, timeout=1)  # open serial port
#         print("sdddddddddddddddddd")
#         print(DevSer.name)  # check which port was really used
#         DevSer.write(b'1234')  # write a string
#         # while True:
#         # x = ser.read()          # read one byte
#         # s = DevSer.read(4)        # read up to ten bytes (timeout)
#         # DevSer.write(b'helo')     # write a string
#         # line = ser.readline()   # read a '\n' terminated line
#         # print(s)
#         self.finished.emit(dev_stat)

