from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from d3model import WindowWith3Dmodel
import myThreads
import sys
import math
import qt_material as qm
import pyvista as pv
from d3model import ellips_zradius
from d3model import RotCalc
from d3model import coil_def_pos
from d3model import coil_model_file_address

tool_x_base = 0
tool_y_base = 0
tool_z_base = 0


class WindowWithDevAN(WindowWith3Dmodel):
    def __init__(self, parent=None):
        super().__init__()
        self.robot_setup_ui()
        self.live_flag = False
        self.an5demoflag = "aaa"
        self.label_robot_pos.setText("X= {:3.1f}mm,      Y= {:3.1f}mm,      Z= {:3.1f}mm".format(0, 0, 0))
        self.label_robot_ang.setText("Rx= {:3.1f}°,      Ry= {:3.1f}°,      Rz= {:3.1f}°".format(int(0),
                                                                                                 int(0),
                                                                                                 int(0)))
        self.headX = 0
        self.headY = 0
        self.headZ = 0
        self.headRx = 0
        self.headRy = 0
        self.headRz = 0
        self.robot_state = "idle"  # reset, drag, getXY, getZ, ready, Start

        self.stim_loc_golb = [0, 0, 0, 0, 0, 0]

    def robot_setup_ui(self):
        self._atuo_pos = 'center'
        self.robot_point = pv.Sphere(radius=10)
        self.actor_robot_point = self.p.add_mesh(self.robot_point, opacity=1, color=[58, 201, 214], name="robot point")
        self.actor_robot_point.SetVisibility(False)

        self.coil_real = pv.read(coil_model_file_address)
        self.coil_real = self.coil_real.rotate_x(90, point=self.axes.origin, inplace=False)
        self.coil_real = self.coil_real.translate(coil_def_pos)
        self.actor_coil_real = self.p.add_mesh(self.coil_real, opacity=1, color=[255, 25, 25], name="coil real")
        self.actor_coil_real.SetVisibility(False)

        self.coil_real_copy = self.coil_real.copy()
        self.actor_coil_copy = self.p.add_mesh(self.coil_real_copy, opacity=1, color=[255, 25, 25],
                                               name="coil real copy")
        self.actor_coil_copy.SetVisibility(False)

        self.pushButton_reset_robot_position.clicked.connect(self.on_reset_robot_bt)
        self.bt_reset_pos.clicked.connect(self.on_reset_robot_bt)
        self.pushButton_drag_robot.clicked.connect(self.on_drag_robot_bt)
        self.pushButton_gather_headxy.clicked.connect(self.on_getxy_robot_bt)
        self.pushButton_gather_headz.clicked.connect(self.on_getz_robot_bt)
        self.pushButton_live_robot_position.clicked.connect(self.on_live_robot_bt)
        self.pushButton_ready_robot_position.clicked.connect(self.on_ready_robot_bt)
        self.bt_cp_poz.clicked.connect(self.on_ready_robot_bt)
        self.pushButton_start_robot_movement.clicked.connect(self.on_start_robot_bt)
        self.StartButton.clicked.connect(self.on_start_robot_bt)

        self.bt_setCz.clicked.connect(self.on_start_auto_cz)
        self.bt_left.clicked.connect(self.on_start_auto_left)
        self.bt_right.clicked.connect(self.on_start_auto_right)
        self.Button_Motion.clicked.connect(self.on_demo)

        # self.label_hx = QLabel("Head Position from Robot Center: x= 0.0mm")
        # self.layout.addWidget(self.label_hx, 1, 15, 1, 1)
        # self.label_hy = QLabel("y= 0.0mm")
        # self.layout.addWidget(self.label_hy, 1, 16, 1, 1)
        # self.label_hz = QLabel("z= 0.0mm")
        # self.layout.addWidget(self.label_hz, 1, 17, 1, 1)

    def on_demo(self):
        print("-------------------------------self.demdem:", self.an5demoflag)
        if self.an5demoflag == "aaa":
            print("maske dem dem True")
            self.an5demoflag = "bbb"
            print(self.an5demoflag)
            print("statttttttttttttttttttttttt demo")
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            print("self.worker.demo_flag", self.worker.demo_flag)
            # self.worker.demo_flag = True
            self.thr.started.connect(self.worker.auto_move_demo)
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()
        else:
            print("stopping 01p-ty")
            self.worker.demo_flag = False
            self.an5demoflag = "aaa"

    def on_start_auto_cz(self):
        my_joint = [81, -90, 111, -115, -91, -101]
        self.thr = QThread()
        self.worker = myThreads.DeviceRobot()
        self.worker.moveToThread(self.thr)
        self.thr.started.connect(lambda: self.worker.auto_move(my_joint, 'n'))
        self.worker.finished.connect(self.robot_state_report)
        self.worker.finished.connect(self.thr.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thr.finished.connect(self.thr.deleteLater)
        self.thr.start()

    def on_start_auto_left(self):
        if self._atuo_pos != 'left':
            my_joint = [101, -84, 113, -114, -133, -13]
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(lambda: self.worker.auto_move(my_joint, 'l'))
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()
            self._atuo_pos = 'left'

    def on_start_auto_right(self):
        if self._atuo_pos != 'right':
            my_joint = [68, -84, 108, -85, -63, -176]
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(lambda: self.worker.auto_move(my_joint, 'r'))
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()
            self._atuo_pos = 'right'

    def on_reset_robot_bt(self):
        self.robot_state = "reset"
        self.robot_motion_threads()

    def on_drag_robot_bt(self):
        self.robot_state = "drag"
        self.robot_motion_threads()

    def on_getxy_robot_bt(self):
        self.robot_state = "getXY"
        self.robot_motion_threads()

    def on_getz_robot_bt(self):
        self.robot_state = "getZ"
        self.robot_motion_threads()

    def on_live_robot_bt(self):
        if self.live_flag:
            self.live_flag = False
            self.actor_robot_point.SetVisibility(False)
            self.actor_coil_copy.SetVisibility(False)
            self.robot_state = "liveOff"
            self.robot_motion_threads()

            self.pushButton_live_robot_position.setText("Start Live Location")
            # self.pushButton_ready_robot_position.setStyleSheet("border-color:#7B5FA2")
            self.pushButton_reset_robot_position.setEnabled(1)
            self.pushButton_drag_robot.setEnabled(1)
            self.pushButton_gather_headxy.setEnabled(1)
            self.pushButton_gather_headz.setEnabled(1)
            self.pushButton_ready_robot_position.setEnabled(1)
            self.pushButton_start_robot_movement.setEnabled(1)
        else:
            self.live_flag = True
            self.actor_robot_point.SetVisibility(True)
            self.actor_coil_copy.SetVisibility(True)
            self.robot_state = "liveOn"
            self.robot_motion_threads()

            self.pushButton_live_robot_position.setText("Stop Live Location")
            # self.pushButton_live_robot_position.setStyleSheet("border-color:#7B9FA2")
            self.pushButton_reset_robot_position.setEnabled(0)
            self.pushButton_drag_robot.setEnabled(0)
            self.pushButton_gather_headxy.setEnabled(0)
            self.pushButton_gather_headz.setEnabled(0)
            self.pushButton_ready_robot_position.setEnabled(0)
            self.pushButton_start_robot_movement.setEnabled(0)

    def on_ready_robot_bt(self):
        self.robot_state = "ready"
        self.robot_motion_threads()

    def on_start_robot_bt(self):
        self.onStartWoMovementButton()
        self.robot_state = "start"
        self.robot_motion_threads()

    def robot_state_machine(self):
        # idle, reset, drag, getXY, getZ, Start
        if self.robot_state == "idle" or self.robot_state == "start":
            self.robot_state = "reset"
            self.pushButton.setText("Enable Drag Mode")

        elif self.robot_state == "reset":
            self.robot_state = "drag"
            self.pushButton.setText("Get Head Coordinates")


        elif self.robot_state == "drag":
            self.robot_state = "getXY"
            self.pushButton.setText("Get Head Height")

        elif self.robot_state == "getXY":
            self.robot_state = "getZ"
            self.pushButton.setText("Go to Ready Point")

        elif self.robot_state == "getZ":
            self.robot_state = "ready"
            self.pushButton.setText("Start")


        elif self.robot_state == "ready":
            self.robot_state = "start"
            self.pushButton.setText("Go to Reset Point")

        self.robot_motion_threads()

    def robot_motion_threads(self):
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
            self.stim_loc_golb[0] = round(-self.Cz_coord[0], 1)
            self.stim_loc_golb[1] = round(-self.Cz_coord[1], 1)
            self.stim_loc_golb[2] = round(self.Cz_coord[2], 1)

            self.stim_loc[3] = 0
            self.stim_loc[4] = 0
            self.stim_loc[5] = 0

            self.stim_loc_golb[3] = round(self.stim_loc[4] - 180, 1)
            self.stim_loc_golb[4] = round(-self.stim_loc[3], 1)
            self.stim_loc_golb[5] = round(self.stim_loc[5] - 90, 1)
            if self.stim_loc_golb[5] < -180:
                self.stim_loc_golb[5] += 360

            print("self.stim_loc_golb:", self.stim_loc_golb)

            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(lambda: self.worker.start(self.stim_loc_golb, 'right'))
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

        if self.robot_state == "liveOn":
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.worker.live_flag = True
            self.thr.started.connect(self.worker.show_live_pos)
            self.worker.progress.connect(self.robot_live_show)
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

        if self.robot_state == "liveOff":
            self.worker.live_flag = False

        if self.robot_state == "start":
            print("coil Location of head center:", self.stim_loc)
            print("self.stim_loc[2]", self.stim_loc[2])
            self.stim_loc_golb[0] = round(-self.headX - self.stim_loc[0], 1)
            self.stim_loc_golb[1] = round(-self.headY - self.stim_loc[1], 1)
            self.stim_loc_golb[2] = round(self.stim_loc[2] + self.headZ, 1)

            if self.stim_loc[4] > 0:
                self.stim_loc_golb[3] = round(self.stim_loc[4] - 180, 1)
            else:
                self.stim_loc_golb[3] = round(self.stim_loc[4] + 180, 1)
            self.stim_loc_golb[4] = round(-self.stim_loc[3], 1)
            self.stim_loc_golb[5] = round(self.stim_loc[5] - 90, 1)
            if self.stim_loc_golb[5] < -180:
                self.stim_loc_golb[5] += 360

            if self.stim_loc[0] < 0:
                self.stim_over_head_flag = 'left'
            else:
                self.stim_over_head_flag = 'right'
            self.thr = QThread()
            self.worker = myThreads.DeviceRobot()
            self.worker.moveToThread(self.thr)
            self.thr.started.connect(lambda: self.worker.start(self.stim_loc_golb, self.stim_over_head_flag))
            self.worker.finished.connect(self.robot_state_report)
            self.worker.finished.connect(self.thr.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.start()

    def robot_live_show(self, coordinates):
        live_robotX = -coordinates[0]
        live_robotY = -coordinates[1]
        live_robotZ = coordinates[2]

        live_robotRx = -coordinates[4]
        if coordinates[3] >= 0:
            live_robotRy = coordinates[3] - 180
        else:
            live_robotRy = coordinates[3] + 180
        live_robotRz = 90 + coordinates[5]
        if live_robotRz >= 180:
            live_robotRz = live_robotRz - 360

        toolx, tooly, toolz = RotCalc.rotate_point(tool_x_base, tool_y_base, tool_z_base,
                                                   live_robotRy, live_robotRx, live_robotRz)
        live_robotX += toolx
        live_robotY += tooly
        live_robotZ += toolz

        XXX = live_robotX - self.headX
        YYY = live_robotY - self.headY
        ZZZ = live_robotZ - self.headZ

        self.label_robot_pos.setText("X= {:3.1f}mm,   Y= {:3.1f}mm,   Z= {:3.1f}mm".format(XXX, YYY, ZZZ))
        self.label_robot_ang.setText("Rx= {:3.1f}mm,   Ry= {:3.1f}mm,   Rz= {:3.1f}mm".format(int(live_robotRx),
                                                                                              int(live_robotRy),
                                                                                              int(live_robotRz)))

        self.robot_point.points += ([XXX, YYY, ZZZ] - self.robot_point.points.mean(0))
        self.coil_real_copy = self.coil_real.copy()
        self.coil_real_copy = self.coil_real_copy.translate([XXX, YYY, ZZZ])
        self.coil_real_copy = self.coil_real_copy.rotate_x(live_robotRx, point=(XXX, YYY, ZZZ))
        self.coil_real_copy = self.coil_real_copy.rotate_y(live_robotRy, point=(XXX, YYY, ZZZ))
        self.coil_real_copy = self.coil_real_copy.rotate_z(live_robotRz, point=(XXX, YYY, ZZZ))
        # self.coil_real_copy = self.coil_real_copy.rotate_x(live_robotRx, point=self.axes.origin)
        # self.coil_real_copy = self.coil_real_copy.rotate_y(live_robotRy, point=self.axes.origin)
        # self.coil_real_copy = self.coil_real_copy.rotate_z(live_robotRz, point=self.axes.origin)
        self.actor_coil_copy = self.p.add_mesh(self.coil_real_copy, opacity=1, color=[87, 87, 87],
                                               name="coil real copy")

    def head_xy_exec(self, coordinates):
        self.Cz_coord = [-coordinates[0], -coordinates[1], coordinates[2]]
        self.headRx = -coordinates[4]
        if coordinates[3] >= 0:
            self.headRy = coordinates[3] - 180
        else:
            self.headRy = coordinates[3] + 180
        self.headRz = 90 + coordinates[5]
        if self.headRz >= 180:
            self.headRz = self.headRz - 360

        self.head_pitch_input.setText(str(int(self.headRx)))
        self.head_roll_input.setText(str(int(self.headRy)))
        self.head_yaw_input.setText(str(int(self.headRz)))

        self.label_head_rx2.setText(str(int(self.headRx)))
        self.label_head_ry2.setText(str(int(self.headRy)))
        self.label_head_rz2.setText(str(int(self.headRz)))

        self.pushButton_gather_headz.setEnabled(True)

    def head_z_exec(self, coordinates):
        self.Cz_coord[2] = coordinates[2]

        toolx, tooly, toolz = RotCalc.rotate_point(tool_x_base, tool_y_base, tool_z_base,
                                                   self.headRy, self.headRx, self.headRz)
        self.Cz_coord[0] += toolx
        self.Cz_coord[1] += tooly
        self.Cz_coord[2] += toolz

        self.headX, self.headY, self.headZ = RotCalc.calculate_sphere_center(self.Cz_coord, self.headRx,
                                                                             self.headRy, self.headRz, ellips_zradius)

        self.label_hx.setText("{:3.1f}mm".format(self.headX))
        self.label_hy.setText("{:3.1f}mm".format(self.headY))
        self.label_hz.setText("{:3.1f}mm".format(self.headZ))

        self.pushButton_ready_robot_position.setEnabled(True)
        self.pushButton_start_robot_movement.setEnabled(True)
        self.StartButton.setEnabled(True)
        self.bt_cp_poz.setEnabled(True)

    def robot_state_report(self):
        pass
        # print("------------------------------------robot move done-------------------------------------------")