import time
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import AN5




class DeviceRobot(QObject):
    finished = pyqtSignal(bool)
    progress = pyqtSignal(list)

    def __init__(self):
        super(DeviceRobot, self).__init__()
        print("thread init")
        print("making demo flag true")
        self.demo_flag = True
        print("self.demo_flag:", self.demo_flag)

        self.live_flag = False
        self.myrobo = AN5.AnnoRobot()
        self.myrobo.connect()
        self.myrobo.reset_error()
        self.myrobo.set_load_wg(3.2)

    def move_readyPoint(self):
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('A')
            # new_pos = self.myrobo.get_TCP_pos()
            # for i in range(len(new_pos)):
            #     new_pos[i] = round(new_pos[i], 1)
            # if new_pos[2] < 400:
            #     new_pos[2] = new_pos[2] + 90
            #     self.myrobo.simple_pos(new_pos, 'left')
            # self.myrobo.simple_joint([90, -100, 30, -45, -90, -90])  # rest point
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.myrobo.disconnect()
            self.finished.emit(True)

    def move_restPoint(self):
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('A')
            # new_pos = self.myrobo.get_TCP_pos()
            # for i in range(len(new_pos)):
            #     new_pos[i] = round(new_pos[i], 1)
            # if new_pos[2] < 400:
            #     new_pos[2] = new_pos[2] + 90
            #     self.myrobo.simple_pos(new_pos, 'left')
            self.myrobo.simple_joint([90, -100, 30, -45, -90, -90])  # rest point
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.myrobo.disconnect()
            self.finished.emit(True)

    def dragEN(self):
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('n')
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.myrobo.disconnect()
            self.finished.emit(False)

    def getXY(self):
        new_pos = [0, 0, 0, 0, 0, 0]
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('n')
            new_pos = self.myrobo.get_TCP_pos()
            self.progress.emit(new_pos)
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.progress.emit(new_pos)
            self.myrobo.disconnect()
            self.finished.emit(False)

    def getZ(self):
        new_pos = [0, 0, 0, 0, 0, 0]
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('A')
            new_pos = self.myrobo.get_TCP_pos()
            self.progress.emit(new_pos)
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.progress.emit(new_pos)
            self.myrobo.disconnect()
            self.finished.emit(False)

    def show_live_pos(self):
        new_pos = [0, 0, 0, 0, 0, 0]
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('n')
            while self.live_flag:
                    new_pos = self.myrobo.get_TCP_pos()
                    self.progress.emit(new_pos)
                    time.sleep(0.2)
            self.myrobo.drag('A')
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.myrobo.disconnect()
            self.finished.emit(False)

    def start(self, stim_loc, flag):
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('A')
            if flag == 'left':
                self.myrobo.simple_joint([-27, -104, -61, 67, -55, -45])

            elif flag == 'right':
                self.myrobo.simple_joint([40, -100, 88, -60, -65, -90])

            print("robot will go to:", stim_loc)
            self.myrobo.simple_pos(stim_loc, flag)
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.myrobo.disconnect()
            self.finished.emit(False)

    def auto_move(self, posit, orit):
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('A')

            new_pos = self.myrobo.get_TCP_pos()
            for i in range(len(new_pos)):
                new_pos[i] = round(new_pos[i], 1)
            if new_pos[2] < 550:
                new_pos[2] = new_pos[2] + 200
                self.myrobo.simple_pos(new_pos, 'right')

            if orit == 'l':
                new_pos = self.myrobo.get_TCP_pos()
                for i in range(len(new_pos)):
                    new_pos[i] = round(new_pos[i], 1)
                new_pos[0] = new_pos[0] + 200
                self.myrobo.simple_pos(new_pos, 'right')

            if orit == 'r':
                new_pos = self.myrobo.get_TCP_pos()
                for i in range(len(new_pos)):
                    new_pos[i] = round(new_pos[i], 1)
                new_pos[0] = new_pos[0] - 200
                self.myrobo.simple_pos(new_pos, 'right')

            self.myrobo.simple_joint(posit)
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.myrobo.disconnect()
            self.finished.emit(False)

    def auto_move_demo(self):
        print("start auto move thread funct:")
        if self.myrobo.robo_connection_stat:
            self.myrobo.drag('A')
            self.demo_flag = True
            print(self.demo_flag, "self.demo_flag")
            # while True:
            print("start while")
            while self.demo_flag == True:
                print("vvvvvvvvvvvvvvvvvvvvvv")
                new_pos = self.myrobo.get_TCP_pos()
                for i in range(len(new_pos)):
                    new_pos[i] = round(new_pos[i], 1)
                if new_pos[2] < 550:
                    new_pos[2] = new_pos[2] + 200
                    self.myrobo.simple_pos(new_pos, 'right')

                posit = [81, -90, 111, -115, -91, -101]  # center
                self.myrobo.simple_joint(posit)
                QThread.sleep(2)

                new_pos = self.myrobo.get_TCP_pos()
                for i in range(len(new_pos)):
                    new_pos[i] = round(new_pos[i], 1)
                if new_pos[2] < 550:
                    new_pos[2] = new_pos[2] + 200
                    self.myrobo.simple_pos(new_pos, 'right')
                posit = [101, -84, 113, -114, -133, -13]
                self.myrobo.simple_joint(posit)
                QThread.sleep(2)

                self.myrobo.simple_joint([90, -100, 30, -45, -90, -90])  # rest point
                QThread.sleep(2)

                self.myrobo.simple_joint([54, -91, 117, -100, -51, -170])  # rest point
                QThread.sleep(2)

                self.myrobo.simple_joint([90, -100, 30, -45, -90, -90])  # rest point
                QThread.sleep(2)
                #
                # QThread.sleep(1)
            print("end finish emit")
            self.myrobo.disconnect()
            self.finished.emit(True)
        else:
            self.myrobo.disconnect()
            self.finished.emit(False)


