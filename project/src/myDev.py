from PyQt5.QtCore import QThread

from ui_loader import Window_ui, motor_real

import myThreads

import serial

from pynput import keyboard


# 90c = 1026 ==> 1c = 11.4


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

class Window_withDev(Window_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setupUi(self)
        self.connectSignalsSlots()
        # self.pushButton_up.setShortcut('w')
        # self.pushButton_down.setShortcut('s')

        try:
            self.DevSer = serial.Serial('COM4', 38400, timeout=1)  # open serial port
        except:
            print("no device found")



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

    def connectSignalsSlots(self):
        self.motor_mvm_connector()
        pass
        # self.pushButton_up.clicked.connect(self.do_Z_up)
        # self.pushButton_down.clicked.connect(self.do_Z_down)


        # self.pushButton_up.pressed.connect(self.do_Z_up)
        # self.pushButton_up.released.connect(self.do_Z_stop)
        # self.pushButton_down.pressed.connect(self.do_Z_down)
        # self.pushButton_down.released.connect(self.do_Z_stop)
        #
        # self.pushButton_set.released.connect(self.do_set_go)
    def motor_mvm_connector(self):

        # self.StartButton.pressed.connect(self.do_set_go)
        self.Z_UpButton.pressed.connect(self.do_Z_up)
        self.Z_UpButton.released.connect(self.do_Z_stop)
        self.Z_DownButton.pressed.connect(self.do_Z_down)
        self.Z_DownButton.released.connect(self.do_Z_stop)

        self.X_LeftButton.pressed.connect(self.do_X_back)
        self.X_LeftButton.released.connect(self.do_Z_stop)
        self.X_RightButton.pressed.connect(self.do_X_forth)
        self.X_RightButton.released.connect(self.do_Z_stop)

        self.Y_ForceButton.pressed.connect(self.do_Y_right)
        self.Y_ForceButton.released.connect(self.do_Z_stop)
        self.Y_BackButton.pressed.connect(self.do_Y_left)
        self.Y_BackButton.released.connect(self.do_Z_stop)

        self.Up_PitchButton.pressed.connect(self.do_alpha_clock)
        self.Up_PitchButton.released.connect(self.do_Z_stop)
        self.Down_PitchButton.pressed.connect(self.do_alpha_count_clock)
        self.Down_PitchButton.released.connect(self.do_Z_stop)

        self.Right_RowButton.pressed.connect(self.do_b_right)
        self.Right_RowButton.released.connect(self.do_Z_stop)
        self.Left_RowButton.pressed.connect(self.do_b_left)
        self.Left_RowButton.released.connect(self.do_Z_stop)


    def do_connect(self):
        self.thread = QThread()
        self.worker = myThreads.DeviceConnect()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.report_connection_stat)
        self.thread.start()



    def DevSerWright(self,val):
        try:
            self.DevSer.write(val)
        except:
            print("error in my dev")



    def do_b_right(self):
        print("bb right")
        self.DevSerWright(b'BrooAAAABBBBCCCC')
        # self.DevSer.write(b'BrooAAAABBBBCCCC')

    def do_b_left(self):
        print("bb left")
        self.DevSerWright(b'BlooAAAABBBBCCCC')
        # self.DevSer.write(b'BlooAAAABBBBCCCC')

    def do_Y_right(self):
        print("right")
        self.DevSerWright(b'YrooAAAABBBBCCCC')
        # self.DevSer.write(b'YrooAAAABBBBCCCC')

    def do_Y_left(self):
        print("left")
        self.DevSerWright(b'YlooAAAABBBBCCCC')
        # self.DevSer.write(b'YlooAAAABBBBCCCC')

    def do_alpha_clock(self):
        print("clockwise")
        self.DevSerWright(b'AcooAAAABBBBCCCC')
        # self.DevSer.write(b'AcooAAAABBBBCCCC')

    def do_alpha_count_clock(self):
        print("counter clockwise")
        self.DevSerWright(b'ACooAAAABBBBCCCC')
        # self.DevSer.write(b'ACooAAAABBBBCCCC')

    def do_X_back(self):
        print("back")
        self.DevSerWright(b'XbooAAAABBBBCCCC')
        # self.DevSer.write(b'XbooAAAABBBBCCCC')

    def do_X_forth(self):
        print("forth")
        self.DevSerWright(b'XfooAAAABBBBCCCC')
        # self.DevSer.write(b'XfooAAAABBBBCCCC')

    def do_Z_up(self):
        print("up")
        self.DevSerWright(b'ZuooAAAABBBBCCCC')
        # self.DevSer.write(b'ZuooAAAABBBBCCCC')

    def do_Z_down(self):
        self.DevSerWright(b'ZdooAAAABBBBCCCC')
        # self.DevSer.write(b'ZdooAAAABBBBCCCC')
        print("down")

    def do_Z_stop(self):
        self.DevSerWright(b'EsooAAAABBBBCCCC')
        # self.DevSer.write(b'EsooAAAABBBBCCCC')
        print("stop")

    def do_set_go(self):    # 71 = g
        intlist = [71, 1, 255, 0, 0, 1, 255, 0, 0, 1, 255, 0, 0, 1, 255, 0]
        try:
            myx = int(self.lineEdit_x.text()) * 40
            myy = int(self.lineEdit_y.text()) * 40
            myz = int(self.lineEdit_z.text())  * 40
            mya = int(self.lineEdit_a.text()) * 11.35
        except:
            print("why?")
            myx = 100
            myy = 100
            myz = 100
            mya = 100

        # myx = 200
        # myy = 200
        # myz = 200
        # mya = 200
        # print(int(myx % 256))
        # intlist = [71, int(myx/256), int(myx%256), 0, 0, int(myy/256), int(myy%256), 0, 1, int(myz/256), unt(myz%256), 0x22, 0, int(mya/256), int(mya%256), 0]
        intlist = [71, int(myx / 256), int(myx % 256), 0, 0, int(myy /256), int(myy % 256), 0, 1,
                   int(myz / 256), int(myz % 256), 0x22, 0, int(mya / 256), int(mya % 256), 0]
        print(intlist)
        print("xmove =========", (intlist[1] * 256) + intlist[2])
        print("ymove =========", (intlist[5] * 256) + intlist[6])
        print("zmove =========", (intlist[9] * 256) + intlist[10])
        print("amove =========", (intlist[13] * 256) + intlist[14])

        bytelist = bytes(intlist)
        self.DevSer.write(bytelist)
        # (48).to_bytes(4, byteorder='big')

    def motor_set(self,  myx, myy, myz, mya, myb):  # 71 = g

        # myy = myy + 15

        if myx != 0:
            myx = - myx
        if myy != 0:
            myy = - myy
        if mya != 0:
            mya = -mya
        if myb != 0:
            myb = - myb



        # myz = myz - 98

        x_dir = 1
        y_dir = 1
        z_dir = 1
        a_dir = 1
        b_dir = 1

        if myx < 0:
            x_dir = 0
        if myy < 0:
            y_dir = 0
        if myz < 0:
            z_dir = 0
        if mya < 0:
            a_dir = 0
        if myb < 0:
            b_dir = 0

        myx = abs(myx) * 40
        myy = abs(myy) * 40
        myz = abs(myz) * 40
        mya = abs(mya) * 11.35
        myb = abs(myb) * 11.05



        intlist = [71, int(myx / 256), int(myx % 256), x_dir,
                   b_dir,
                   int(myy / 256), int(myy % 256), y_dir,
                   int(myb / 256),
                   int(myz / 256), int(myz % 256), z_dir,
                   int(myb % 256),
                   int(mya / 256), int(mya % 256), a_dir]

        print(intlist)
        print("xmove =========", (intlist[1] * 256) + intlist[2])
        print("ymove =========", (intlist[5] * 256) + intlist[6])
        print("zmove =========", (intlist[9] * 256) + intlist[10])
        print("amove =========", (intlist[13] * 256) + intlist[14])

        bytelist = bytes(intlist)
        if motor_real:
            self.DevSer.write(bytelist)
        # (48).to_bytes(4, byteorder='big')