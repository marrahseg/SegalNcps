import time
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import AN5


myrobo = AN5.AnnoRobot()
myrobo.connect()
myrobo.reset_error()

class DeviceRobot(QObject):
    finished = pyqtSignal(bool)
    progress = pyqtSignal(float, float)

    def __init__(self):
        super(DeviceRobot, self).__init__()
        # self.myrobo = AN5.AnnoRobot()
        # self.myrobo.connect()
        # self.myrobo.reset_error()


    def run(self):
        self.finished.emit(dev_stat)

    def move_restPoint(self):
        myrobo.drag('A')
        new_pos = myrobo.get_TCP_pos()
        if new_pos[2] < 600:
            new_pos[2] = new_pos[2] + 90
            myrobo.simple_pos(new_pos)
        myrobo.simple_joint([74, -100, 40, -25, -90, 45])  # rest point
        self.finished.emit(True)

    def dragEN(self):
        myrobo.drag('n')
        self.finished.emit(True)

    def getXY(self):
        myrobo.drag('n')
        new_pos = myrobo.get_TCP_pos()
        self.progress.emit(new_pos[0], new_pos[1])
        self.finished.emit(True)

    def getZ(self):
        myrobo.drag('A')
        new_pos = myrobo.get_TCP_pos()
        self.progress.emit(new_pos[2], 0)
        self.finished.emit(True)

    def start(self, x, y, z, xx, yy, zz):
        myrobo.drag('A')
        radd = 140
        ppos = myrobo.goto_head_pos(x, y, z - radd, xx, yy, zz, radd)
        print("ppos:", ppos)

        zflag = 0
        if ppos[2] < 600:
            ppos[2] = ppos[2] + 90
            zflag = 1
        myrobo.simple_pos(ppos)

        if zflag == 1:
            new_pos = myrobo.get_TCP_pos()
            new_pos[2] = new_pos[2] - 90
            myrobo.simple_pos(new_pos)

        self.finished.emit(True)
