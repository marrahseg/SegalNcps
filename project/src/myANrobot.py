from PyQt5.QtCore import QThread

from ui_loader import Window_ui, motor_real

import myThreads

import serial

from pynput import keyboard


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


class Window_withDevAN(Window_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connectSignalsSlots()
        self.headX = 0
        self.headY = 0
        self.headZ = 0
        self.robot_state = "idle"  # reset, drag, getXY, getZ, ready, Start

    def onGoMotionRobot(self):
        # idle, reset, drag, getXY, getZ, Start
        if self.robot_state == "idle" or self.robot_state == "start":
            self.robot_state = "reset"
            self.pushButton.setText("Enable Drag")

        elif self.robot_state == "reset":
            self.robot_state = "drag"
            self.pushButton.setText("Get X , Y")


        elif self.robot_state == "drag":
            self.robot_state = "getXY"
            self.pushButton.setText("Get Z")

        elif self.robot_state == "getXY":
            self.robot_state = "getZ"
            self.pushButton.setText("Ready Point")

        elif self.robot_state == "getZ":
            self.robot_state = "ready"
            self.pushButton.setText("Start")


        elif self.robot_state == "ready":
            self.robot_state = "start"
            self.pushButton.setText("Go to reset point")


        self.robot_state_machine()

    def robot_state_machine(self):
        # idle, reset, drag, getXY, getZ, ready, Start
        if self.robot_state == "idle":
            pass
        if self.robot_state == "reset":
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(self.worker.move_restPoint)
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

        if self.robot_state == "drag":
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(self.worker.dragEN)
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

        if self.robot_state == "getXY":
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(self.worker.getXY)
            self.worker.progress.connect(self.head_xy_exec)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

        if self.robot_state == "getZ":
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(self.worker.getZ)
            self.worker.progress.connect(self.head_z_exec)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

        if self.robot_state == "ready":
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(self.worker.move_restPoint)
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

        if self.robot_state == "start":
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(lambda: self.worker.start(self.headX, self.headY, self.headZ,
                                                               self.XSpin.value(), self.YSpin.value(), self.ZSpin.value()))
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

    def head_xy_exec(self, x, y):
        self.headX = x
        self.headY = y
        print("new x , y pos of the head: ", x, ",", y)

    def head_z_exec(self, z, w):
        self.headZ = z
        print("new z pos of the head: ", z)

    def robot_state_report(self):
        print("------------------------------------robot move done-------------------------------------------")

    def connectSignalsSlots(self):
        pass

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        pressed = event.key()
        print("pres: ", pressed)

        if pressed == 87:  # 87=w
            self.do_Z_up()
        if pressed == 83:  # 83=s
            self.do_Z_down()
        if pressed == 65:  # 65=a
            self.do_alpha_count_clock()
        if pressed == 68:  # 68=d
            self.do_alpha_clock()
        if pressed == 76:  # 76=76
            self.do_X_back()
        if pressed == 74:  # 52=4
            self.do_X_forth()
        if pressed == 75:  # 56=8 up
            self.do_Y_right()
        if pressed == 73:  # 50=2 bot
            self.do_Y_left()

        if pressed == 88:  # 50=2 bot
            self.do_b_left()
        if pressed == 90:  # 50=2 bot
            self.do_b_right()

        event.accept()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        released = event.key()
        print(released)

        if released == 87:  # 87=w
            self.do_Z_stop()
        if released == 83:  # 83=s
            self.do_Z_stop()
        if released == 65:  # 65=a
            self.do_Z_stop()
        if released == 68:  # 68=d
            self.do_Z_stop()
        if released == 74:  # 74=j
            self.do_Z_stop()
        if released == 76:  # 76=l
            self.do_Z_stop()
        if released == 75:  # 75=k up
            self.do_Z_stop()
        if released == 73:  # 73=i bot
            self.do_Z_stop()
        if released == 88:  # 75=k up
            self.do_Z_stop()
        if released == 90:  # 73=i bot
            self.do_Z_stop()
        event.accept()
