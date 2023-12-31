import socket
import time
import numpy as np
from math import pi
import re  # string finding library
import math
from visual_kinematics.RobotSerial import *

coil_weight = 3.2
pp = np.pi / 2
dh_params = np.array([[151, 0., pp, 0.],
                      [138, -426, 0., 0.],
                      [-138, -395, 0., 0.],
                      [130, 0., pp, 0],
                      [102, 0., -pp, 0.],
                      [100, 0., 0., 0.]])
robot = RobotSerial(dh_params)


def joint_to_position(joint_angles):
    joint_angles_rad = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        joint_angles_rad[i] = np.radians(joint_angles[i])
    theta = np.array([joint_angles_rad[0], joint_angles_rad[1], joint_angles_rad[2],
                      joint_angles_rad[3], joint_angles_rad[4], joint_angles_rad[5]])
    f = robot.forward(theta)

    mpos = [0, 0, 0, 0, 0, 0]
    mpos[0] = round(f.t_3_1.reshape([3, ])[0], 3)
    mpos[1] = round(f.t_3_1.reshape([3, ])[1], 3)
    mpos[2] = round(f.t_3_1.reshape([3, ])[2], 3)
    mpos[3] = round(np.degrees(f.euler_3[2]), 3)
    mpos[4] = round(np.degrees(f.euler_3[1]), 3)
    mpos[5] = round(np.degrees(f.euler_3[0]), 3)

    return mpos


def position_to_joint(positions):
    xyz = np.array([[positions[0]], [positions[1]], [positions[2]]])
    abc = np.array([np.radians(positions[3]), np.radians(positions[4]), np.radians(positions[5])])
    end = Frame.from_euler_3(abc, xyz)
    robot.inverse(end)
    mJoints = [0, 0, 0, 0, 0, 0]
    mJoints[0] = np.round(np.degrees(robot.axis_values[0]), 3)
    mJoints[1] = np.round(np.degrees(robot.axis_values[1]), 3)
    mJoints[2] = np.round(np.degrees(robot.axis_values[2]), 3)
    mJoints[3] = np.round(np.degrees(robot.axis_values[3]), 3)
    mJoints[4] = np.round(np.degrees(robot.axis_values[4]), 3)
    mJoints[5] = np.round(np.degrees(robot.axis_values[5]), 3)

    return robot.is_reachable_inverse, mJoints


class AnnoRobot:
    def __init__(self):
        super().__init__()
        self.robo_connection_stat = False
        self.robot_response = None
        self.myIPAddr = None
        self.myhostname = None
        self.rHOST = "192.168.58.2"  # The server's hostname or IP address
        self.rPORT = 8080  # The port used by the server

    def connect(self):
        self.myhostname = socket.gethostname()
        self.myIPAddr = socket.gethostbyname(self.myhostname)
        print("PC Host Name:", self.myhostname)
        print("PC IP Address:", self.myIPAddr)
        self.roboSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.roboSocket.settimeout(20)
        try:
            self.roboSocket.connect((self.rHOST, self.rPORT))
            self.robo_connection_stat = True
            print("AN5 Robot Succecss fully connected")
        except:
            print("AN5: Cant connect to robot please check LAN Connection")
            self.robo_connection_stat = False

    def disconnect(self):
        self.roboSocket.close()

    def cmd_generator(self, cmd_cnt, cmd_idf, cmd_string):
        cmd_len = len(cmd_string)
        new_cmd = ["/f/b", "III", cmd_cnt, "III", cmd_idf, "III", cmd_len, "III", cmd_string, "III", "/b/f"]
        cmd_str = "".join(map(str, new_cmd))
        cmd_byte = bytes(cmd_str, 'utf-8')
        return cmd_byte

    def send_cmd(self, cmd_byte):
        if self.robo_connection_stat:
            # print(cmd_byte)
            self.roboSocket.send(cmd_byte)

            self.robot_response = self.roboSocket.recv(1024)
            ret_str = str(self.robot_response)
            if ret_str.find("errcode") != -1:
                print("Return Data --->", self.robot_response)

    def reset_error(self):
        my_cmd = self.cmd_generator(cmd_cnt=2, cmd_idf=107, cmd_string="RESETALLERROR")
        self.send_cmd(my_cmd)

    def set_load_wg(self, wg):
        my_cmd = self.cmd_generator(cmd_cnt=4, cmd_idf=306, cmd_string="SetLoadWeight(" + str(wg) + ")")
        self.send_cmd(my_cmd)

    def start(self):
        my_cmd = self.cmd_generator(cmd_cnt=4, cmd_idf=101, cmd_string="START")
        self.send_cmd(my_cmd)

    def mode(self, rmod="A"):
        if rmod == "A":
            my_cmd = self.cmd_generator(cmd_cnt=0, cmd_idf=303, cmd_string="Mode(0)")
            self.send_cmd(my_cmd)
        else:
            my_cmd = self.cmd_generator(cmd_cnt=0, cmd_idf=303, cmd_string="Mode(1)")
            self.send_cmd(my_cmd)

    def drag(self, rdrag="A"):
        if rdrag == "A":
            my_cmd = self.cmd_generator(cmd_cnt=1, cmd_idf=333, cmd_string="DragTeachSwitch(0)")
            self.send_cmd(my_cmd)
        else:
            my_cmd = self.cmd_generator(cmd_cnt=1, cmd_idf=333, cmd_string="DragTeachSwitch(1)")
            self.send_cmd(my_cmd)

    def get_TCP_pos(self):
        my_cmd = self.cmd_generator(cmd_cnt=3, cmd_idf=377, cmd_string="GetActualTCPPose()")
        self.send_cmd(my_cmd)
        robo_data = self.robot_response.decode()
        # float_pattern = r'[-+]?\d*\.\d+|\d+'
        float_pattern = r'[-+]?\d*\.\d+'
        float_list = re.findall(float_pattern, robo_data)
        float_list = [float(num) for num in float_list]
        return float_list

    def get_TCP_num(self):
        my_cmd = self.cmd_generator(cmd_cnt=3, cmd_idf=377, cmd_string="GetActualTCPNum()")
        self.send_cmd(my_cmd)

    def get_inv_kin(self, positions, optim_joint):
        cmd_name = "GetInverseKin"
        data_str = "0, "
        for i in positions:
            data_str += str(i) + ","
        cmd_str = cmd_name + "(" + data_str[:-1] + "," + str(optim_joint) + ")"
        my_cmd = self.cmd_generator(cmd_cnt=3, cmd_idf=377, cmd_string=cmd_str)
        self.send_cmd(my_cmd)
        robo_data = self.robot_response.decode()
        # float_pattern = r'[-+]?\d*\.\d+|\d+'
        float_pattern = r'[-+]?\d*\.\d+'
        float_list = re.findall(float_pattern, robo_data)
        float_list = [float(num) for num in float_list]
        return float_list

    # mode: 0-joint cordinate, 2-base cordinate, 4-tool cordinates
    def single_move(self, mode, jnum, direct, speed, distance):
        cmd_idf = 232
        cmd_name = "StartJOG"
        acc = 60

        cmd_data = [mode, jnum, direct, speed, acc, distance]
        data_str = ""
        for i in cmd_data:
            data_str += str(i) + ","

        cmd_str = cmd_name + "(" + data_str[:-1] + ")"
        my_cmd = self.cmd_generator(21, cmd_idf, cmd_str)
        self.send_cmd(my_cmd)

    # move tohtough an axis with give axis, direction ad range
    def simple_cart(self, loc, direct, speed, mm):
        jnum = 10
        dir = 10
        if loc == 'x':
            jnum = 1
            if direct == 'r' or direct == '-':
                dir = 0
            else:
                dir = 1
        if loc == 'y':
            jnum = 2
            if direct == 'f' or direct == '-':
                dir = 0
            else:
                dir = 1
        if loc == 'z':
            jnum = 3
            if direct == 'd' or direct == '-':
                dir = 0
            else:
                dir = 1
        if loc == 'rx':
            jnum = 4
            if direct == '-':
                dir = 0
            else:
                dir = 1
        if loc == 'ry':
            jnum = 5
            if direct == '-':
                dir = 0
            else:
                dir = 1
        if loc == 'rz':
            jnum = 6
            if direct == '-':
                dir = 0
            else:
                dir = 1
        self.single_move(mode=2, jnum=jnum, direct=dir, speed=speed, distance=mm)

    # move to a position with given joint angles and final positions
    def movej(self, joints, positions, speed):
        x = positions[0]
        y = positions[1]
        z = positions[2]
        rx = positions[3]
        ry = positions[4]
        rz = positions[5]

        j1 = joints[0]
        j2 = joints[1]
        j3 = joints[2]
        j4 = joints[3]
        j5 = joints[4]
        j6 = joints[5]
        cmd_idf = 201
        cmd_name = "MoveJ"
        toolNum = int(0)
        workPieceNum = int(0)
        acc = 50
        ovl = 95
        blendT = -1
        exaxisPos1 = 0.00
        exaxisPos2 = 0.00
        exaxisPos3 = 0.00
        exaxisPos4 = 0.00
        offset_flag = 4
        dt_x = 0.0
        dt_y = 0.0
        dt_z = 0.0
        dt_rx = 0.0
        dt_ry = 0.0
        dt_rz = 0.0

        cmd_data = [j1, j2, j3, j4, j5, j6, x, y, z, rx, ry, rz, toolNum, workPieceNum, speed, acc, ovl,
                    exaxisPos1, exaxisPos2, exaxisPos3, exaxisPos4, blendT, offset_flag, dt_x, dt_y, dt_z, dt_rx, dt_ry,
                    dt_rz]
        data_str = ""
        for i in cmd_data:
            data_str += str(i) + ","

        cmd_str = cmd_name + "(" + data_str[:-1] + ")"
        my_cmd = self.cmd_generator(21, cmd_idf, cmd_str)

        self.send_cmd(my_cmd)

    # move to a position with given x,y,z,rx,ry,rz
    def simple_pos(self, positions, flag):
        if flag == 'right':
            optim_joint = -1
        else:
            optim_joint = 1

        joints = self.get_inv_kin(positions, optim_joint)
        if len(joints) < 5:
            print("some error happened, inverse kinematic calculation failed?")
            print("                 ---> joint values:", joints)
            print("tray again with new roll value ...")
            positions[4] += positions[4] + 15

            joints = self.get_inv_kin(positions, optim_joint)
            if len(joints) < 5:
                print("This is serious one :(")
            else:
                self.movej(joints, positions, 30)
        else:
            self.movej(joints, positions, 30)



    # move to a position with given hoint angles
    def simple_joint(self, joints):
        pos = joint_to_position(joints)
        self.movej(joints, positions=pos, speed=40)
