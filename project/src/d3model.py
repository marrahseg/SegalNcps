import sys
import math
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import qt_material as qm
from ui_loader import Window_ui
head_file_name = '../UI/STL/Head-1.stl'
coil_model_file_address = '../UI/STL/Coil TMS v0.stl'
stim_line_extension_scale = 1000
headObj_opacity = 0.6
head_stl_scale = 0.65

coil_z = 0
coil_def_pos = [-34, 20, -coil_z]

head_center_adjustment_y = -14.41

ellips_xradius = 55 + coil_z
ellips_yradius = 75 + coil_z
ellips_zradius = 90 + coil_z

sphere_radius = ellips_zradius
head_center_adjustment_y = head_center_adjustment_y * (ellips_yradius / 212) / 2


class RotCalc(object):
    @staticmethod
    def rotate_point(x, y, z, roll, pitch, yaw):
        """
        Rotate a point in 3D space based on pitch, roll, and yaw angles.

        Args:
            x: x-coordinate of the point.
            y: y-coordinate of the point.
            z: z-coordinate of the point.
            pitch: Pitch angle in degrees.
            roll: Roll angle in degrees.
            yaw: Yaw angle in degrees.

        Returns:
            The new (x', y', z') coordinates of the rotated point.
        """
        # Convert angles to radians
        pitch_rad = math.radians(pitch)
        roll_rad = math.radians(roll)
        yaw_rad = math.radians(yaw)

        # Define rotation matrices
        rotation_pitch = np.array([
            [1, 0, 0],
            [0, math.cos(pitch_rad), -math.sin(pitch_rad)],
            [0, math.sin(pitch_rad), math.cos(pitch_rad)]
        ])

        rotation_roll = np.array([
            [math.cos(roll_rad), 0, math.sin(roll_rad)],
            [0, 1, 0],
            [-math.sin(roll_rad), 0, math.cos(roll_rad)]
        ])

        rotation_yaw = np.array([
            [math.cos(yaw_rad), -math.sin(yaw_rad), 0],
            [math.sin(yaw_rad), math.cos(yaw_rad), 0],
            [0, 0, 1]
        ])

        # Apply rotations
        rotated_point = np.dot(rotation_pitch, np.array([x, y, z]))
        rotated_point = np.dot(rotation_roll, rotated_point)
        rotated_point = np.dot(rotation_yaw, rotated_point)

        # Extract new coordinates
        x_new, y_new, z_new = rotated_point

        return x_new, y_new, z_new

    @staticmethod
    def ellipsoid_surface_point(x, y, z):
        """
        Compute intersection of a given point (head of a vector) and the ellipsoid.

        Args:
            x: x-coordinate of the point.
            y: y-coordinate of the point.
            z: z-coordinate of the point.

        Returns:
            The new (x', y', z') coordinates of the collision point.
        """
        # normalize the vector base on the ellipsoid's radiuses
        vector_x = x / ellips_xradius
        vector_y = y / ellips_yradius
        vector_z = z / ellips_zradius

        # Calculate the magnitude of the vector
        magnitude = math.sqrt(vector_x ** 2 + vector_y ** 2 + vector_z ** 2)

        # Generate the unity vector
        unit_vector_x = vector_x / magnitude
        unit_vector_y = vector_y / magnitude
        unit_vector_z = vector_z / magnitude

        # Calculate the coordinates of the surface point
        surface_x = round(unit_vector_x * ellips_xradius, 3)
        surface_y = round(unit_vector_y * ellips_yradius, 3)
        surface_z = round(unit_vector_z * ellips_zradius, 3)

        return surface_x, surface_y, surface_z

    @staticmethod
    def ellipsoid_surface_angle(x, y, z):
        # Convert Cartesian coordinates to unit vector
        magnitude = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        unit_vector = np.array([x / magnitude, y / magnitude, z / magnitude])

        # Calculate the normal vector of the tangent plane
        normal_vector = np.array([unit_vector[0] / ellips_xradius ** 2, unit_vector[1] / ellips_yradius ** 2,
                                  unit_vector[2] / ellips_zradius ** 2])
        normal_vector /= np.linalg.norm(normal_vector)

        # Calculate the tangent surface angles
        theta = np.arccos(normal_vector[2])
        phi = np.arctan2(normal_vector[1], normal_vector[0])

        theta = round(math.degrees(theta), 1)
        phi = round(math.degrees(phi), 1)
        return theta, phi

    @staticmethod
    def ellipsoid_surface_angle_old_version(x, y, z):
        # Normalize the coordinates
        x_normalized = x / ellips_xradius
        y_normalized = y / ellips_yradius
        z_normalized = z / ellips_zradius

        # Calculate the azimuthal angle (φ)
        phi = math.atan2(y_normalized, x_normalized)
        # Calculate the polar(Altitude) angle (θ)
        r_normalized = math.sqrt(x_normalized ** 2 + y_normalized ** 2 + z_normalized ** 2)
        # r_normalized = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        theta = math.acos(z_normalized / r_normalized)

        theta = round(math.degrees(theta), 1)
        phi = round(math.degrees(phi), 1)
        return theta, phi

    @staticmethod
    def sphere_surface_point(x, y, z):
        # Calculate the vector from the center to the input point
        center_x = 0
        center_y = 0
        center_z = 0
        vector_x = x - center_x
        vector_y = y - center_y
        vector_z = z - center_z

        # Calculate the magnitude of the vector
        magnitude = math.sqrt(vector_x ** 2 + vector_y ** 2 + vector_z ** 2)

        if magnitude != 0:
            # Calculate the unit vector pointing from the center to the input point
            unit_vector_x = vector_x / magnitude
            unit_vector_y = vector_y / magnitude
            unit_vector_z = vector_z / magnitude
        else:
            unit_vector_x = vector_x
            unit_vector_y = vector_y
            unit_vector_z = vector_z
        # Calculate the coordinates of the surface point
        surface_x = center_x + unit_vector_x * sphere_radius
        surface_y = center_y + unit_vector_y * sphere_radius
        surface_z = center_z + unit_vector_z * sphere_radius

        # Convert the coordinates and angles to millimeters and degrees with 3 digits precision
        surface_x_mm = round(surface_x, 3)
        surface_y_mm = round(surface_y, 3)
        surface_z_mm = round(surface_z, 3)

        ################################################
        phi = math.atan2(unit_vector_y, unit_vector_x)
        # Calculate the polar angle (θ)
        r = math.sqrt(unit_vector_x ** 2 + unit_vector_y ** 2 + unit_vector_z ** 2)
        theta = math.acos(unit_vector_z / r)
        # print("phi:", math.degrees(phi), "theta:", math.degrees(theta))
        rx = 0
        ry = round(math.degrees(theta), 1)
        rz = round(math.degrees(phi), 1)

        # return [surface_x_mm, surface_y_mm, surface_z_mm, rx, ry, rz]
        return surface_x_mm, surface_y_mm, surface_z_mm
        # print("surface_x, surface_y, surface_z:", surface_x, surface_y, surface_z)
        # return surface_x, surface_y, surface_z

    @staticmethod
    def sphere_surface_angle(x, y, z):
        unit_vector_x = x
        unit_vector_y = y
        unit_vector_z = z

        ################################################
        phi = math.atan2(unit_vector_y, unit_vector_x)
        # Calculate the polar angle (θ)
        r = math.sqrt(unit_vector_x ** 2 + unit_vector_y ** 2 + unit_vector_z ** 2)
        theta = math.acos(unit_vector_z / r)
        rx = 0
        theta = round(math.degrees(theta), 1)
        phi = round(math.degrees(phi), 1)
        # print("Sphere theta, phi:", theta, phi)
        return theta, phi

    @staticmethod
    def calculate_sphere_center(plane_center, pitch, roll, yaw, radius):
        # Convert pitch, roll, and yaw angles to radians
        pitch_rad = np.radians(pitch)
        roll_rad = np.radians(roll)
        yaw_rad = np.radians(yaw)

        # Extract plane center coordinates
        x_p, y_p, z_p = plane_center

        # Calculate rotation matrices
        R_pitch = np.array([[1, 0, 0],
                            [0, np.cos(pitch_rad), -np.sin(pitch_rad)],
                            [0, np.sin(pitch_rad), np.cos(pitch_rad)]])

        R_roll = np.array([[np.cos(roll_rad), 0, np.sin(roll_rad)],
                           [0, 1, 0],
                           [-np.sin(roll_rad), 0, np.cos(roll_rad)]])

        R_yaw = np.array([[np.cos(yaw_rad), -np.sin(yaw_rad), 0],
                          [np.sin(yaw_rad), np.cos(yaw_rad), 0],
                          [0, 0, 1]])

        # Calculate combined rotation matrix
        R = R_yaw @ R_roll @ R_pitch

        # Calculate transformed normal vector
        n = np.array([0, 0, 1])  # Normal vector of the plane (assuming it is aligned with the z-axis)
        n_transformed = R @ n

        # Calculate sphere center
        C = -n_transformed
        scaled_C = radius * C
        sphere_center = plane_center + scaled_C

        return round(sphere_center[0], 1), round(sphere_center[1], 1), round(sphere_center[2], 1)


class WindowWith3Dmodel(Window_ui):
    def __init__(self):
        super().__init__()
        self.actor_sphere = None
        self.setup_ui()
        self.slot_connect()
        self.initiate_3d_modules()

        self.head_pitch = 0  # head angel in x axis degree
        self.head_roll = 0  # head angel in y axis degree
        self.head_yaw = 0  # head angel in z axis degree
        self.ellip_x = 0
        self.ellip_y = 0
        self.ellip_z = 0

        self.stimP_x = 0
        self.stimP_y = 0
        self.stimP_z = 1

        self.stim_loc = [0, -300, 300, 0, 0, 0]

    def setup_ui(self):
        self.p = QtInteractor()
        self.verticalLayout_23.addWidget(self.p)

    def slot_connect(self):
        self.bt_setPoint.clicked.connect(self.on_set_stim_point)
        self.bt_setRotation.clicked.connect(self.on_set_head_angle)
        # self.pushButton_reset_angels.clicked.connect(self.on_reset_head_angle)
        self.bt_clac_spot.clicked.connect(self.on_calculate_stim_position)
        self.bt_view_main_axis.clicked.connect(self.hide_axis_main)
        self.bt_view_sphere.clicked.connect(self.hide_stim_area)
        self.bt_view_headbrain.clicked.connect(self.hide_head_brain)
        self.bt_zoom_in.clicked.connect(self.on_zoom_in)
        self.bt_zoom_out.clicked.connect(self.on_zoom_out)

    def on_calculate_stim_position(self):
        self.xPoint_cal, self.yPoint_cal, self.zPoint_cal = \
            RotCalc.rotate_point(self.stimP_x, self.stimP_y, self.stimP_z, self.head_roll, self.head_pitch,
                                 self.head_yaw)

        self.xlabel1.setText("x= {:3.1f}mm".format(self.xPoint_cal))
        self.ylabel1.setText("y= {:3.1f}mm".format(self.yPoint_cal))
        self.zlabel1.setText("z= {:3.1f}mm".format(self.zPoint_cal))

        self.XSpin.setValue(round(self.xPoint_cal, 1))
        self.YSpin.setValue(round(self.yPoint_cal, 1))
        self.ZSpin.setValue(round(self.zPoint_cal, 1))


        self.point1.SetCenter(self.xPoint_cal, self.yPoint_cal, self.zPoint_cal)
        self.center_line = pv.Line((0, 0, 0),
                                   (self.xPoint_cal * stim_line_extension_scale,
                                    self.yPoint_cal * stim_line_extension_scale,
                                    self.zPoint_cal * stim_line_extension_scale))
        self.p.add_mesh(self.center_line, color='y', name="point_line", line_width=10)

        # ############ Calculate stim point on the ellipsoid
        self.ellip_x, self.ellip_y, self.ellip_z = RotCalc.ellipsoid_surface_point(self.stimP_x, self.stimP_y,
                                                                    self.stimP_z)

        self.ellip_x, self.ellip_y, self.ellip_z = \
            RotCalc.rotate_point(self.ellip_x, self.ellip_y, self.ellip_z, self.head_roll, self.head_pitch, self.head_yaw)

        self.ry_ellips, self.rz_ellips = RotCalc.ellipsoid_surface_angle(self.ellip_x, self.ellip_y, self.ellip_z)


        # ############ Calculate stim point on the sphere
        px, py, pz = RotCalc.sphere_surface_point(self.xPoint_cal, self.yPoint_cal, self.zPoint_cal)
        ry, rz = RotCalc.sphere_surface_angle(self.xPoint_cal, self.yPoint_cal, self.zPoint_cal)



        # ################################################################################ Show stim coil and point
        if self.actor_sphere.GetVisibility():
            self.stim_point = pv.Sphere(radius=7, center=(px, py, pz))
            self.actor_stim_point = self.p.add_mesh(self.stim_point, opacity=1, color=[58, 201, 214], name="stim point")
            self.actor_stim_point.SetVisibility(True)

            # Reset coil position on 0,0,0
            self.coil = pv.read('Coil TMS v0.stl')
            self.coil = self.coil.rotate_x(90, point=self.axes.origin, inplace=False)
            self.coil = self.coil.translate(coil_def_pos)

            self.coil = self.coil.translate([px, py, pz])
            # self.coil = self.coil.rotate_x(rx, point=(px, py, pz))
            self.coil = self.coil.rotate_y(ry, point=(px, py, pz))
            self.coil = self.coil.rotate_z(rz, point=(px, py, pz))
            self.actor_coil = self.p.add_mesh(self.coil, opacity=1, color=[58, 113, 214], name="coil")
            self.stim_loc = [px, py, pz, 0, ry, rz]
            print("self.stim_loc:", self.stim_loc)

        elif self.actor_ellips.GetVisibility():
            # Show stim point on ellipsoid
            self.stim_point_ellip = pv.Sphere(radius=7, center=(self.ellip_x, self.ellip_y, self.ellip_z))
            self.actor_stim_point_ellip = self.p.add_mesh(self.stim_point_ellip, opacity=1, color=[235, 118, 2],
                                                          name="stim point ellip")

            # Reset coil position on 0,0,0
            self.coil = pv.read('Coil TMS v0.stl')
            self.coil = self.coil.rotate_x(90, point=self.axes.origin, inplace=False)
            self.coil = self.coil.translate(coil_def_pos)

            self.coil = self.coil.translate([self.ellip_x, self.ellip_y, self.ellip_z])
            # self.coil = self.coil.rotate_x(rx, point=(px, py, pz))
            self.coil = self.coil.rotate_y(self.ry_ellips, point=(self.ellip_x, self.ellip_y, self.ellip_z))
            self.coil = self.coil.rotate_z(self.rz_ellips, point=(self.ellip_x, self.ellip_y, self.ellip_z))
            self.actor_coil = self.p.add_mesh(self.coil, opacity=1, color=[58, 113, 214], name="coil")


            self.stim_loc = [self.ellip_x, self.ellip_y, self.ellip_z, 0, self.ry_ellips, self.rz_ellips]
            print("self.stim_loc:", self.stim_loc)

    def on_reset_head_angle(self):
        self.head_roll_input.setText("0")
        self.head_pitch_input.setText("0")
        self.head_yaw_input.setText("0")
        self.on_set_head_angle()

    def on_set_head_angle(self):
        if self.head_pitch != 0:
            rx = -self.head_pitch
        else:
            rx = 0
        if self.head_roll != 0:
            ry = -self.head_roll
        else:
            ry = 0
        if self.head_yaw != 0:
            rz = -self.head_yaw
        else:
            rz = 0
        self.execute_head_rotations(rx, ry, rz, False)

        self.head_pitch = int(self.head_pitch_input.text())
        self.head_roll = int(self.head_roll_input.text())
        self.head_yaw = int(self.head_yaw_input.text())
        self.execute_head_rotations(self.head_pitch, self.head_roll, self.head_yaw)

    def on_set_stim_point(self):
        self.onStartWoMovementButton()
        self.stimP_x = self.XSpin.value()
        self.stimP_y = self.YSpin.value()
        self.stimP_z = self.ZSpin.value()

        if self.stimP_x + self.stimP_y + self.stimP_z == 0:
            self.stimP_z = 1

        self.xlabel1.setText("x= {:3.1f}mm".format(self.stimP_x))
        self.ylabel1.setText("y= {:3.1f}mm".format(self.stimP_y))
        self.zlabel1.setText("z= {:3.1f}mm".format(self.stimP_z))
        self.point1.SetCenter(self.stimP_x, self.stimP_y, self.stimP_z)


        self.center_line = pv.Line((0, 0, 0),
                                   (self.stimP_x * stim_line_extension_scale,
                                    self.stimP_y * stim_line_extension_scale,
                                    self.stimP_z * stim_line_extension_scale))
        self.p.add_mesh(self.center_line, color='y', name="point_line", line_width=10)

    def execute_head_rotations(self, pi, ro, ya, exec_show=True):

        # for rotation of head
        if exec_show:
            self.rot_body = self.rot_body.rotate_x(pi, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)
            self.rot_body = self.rot_body.rotate_y(ro, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)
            self.rot_body = self.rot_body.rotate_z(ya, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)

            self.actor_head = self.p.add_mesh(self.rot_body, color=(158, 158, 158), specular=0.7,
                            specular_power=15, ambient=0.8, smooth_shading=True, opacity=headObj_opacity,
                            name="rot_body")
        else:
            self.rot_body = self.rot_body.rotate_z(ya, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)
            self.rot_body = self.rot_body.rotate_y(ro, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)
            self.rot_body = self.rot_body.rotate_x(pi, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)

        # for rotation of brain
        if exec_show:
            self.rot_brain = self.rot_brain.rotate_x(pi, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)
            self.rot_brain = self.rot_brain.rotate_y(ro, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)
            self.rot_brain = self.rot_brain.rotate_z(ya, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)

            self.actor_brain = self.p.add_mesh(self.rot_brain, color=(55, 55, 55), specular=0.7,
                                               specular_power=15, ambient=0.8, smooth_shading=True, opacity=1,
                                               name="rot_brain")
        else:
            self.rot_brain = self.rot_brain.rotate_z(ya, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)
            self.rot_brain = self.rot_brain.rotate_y(ro, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)
            self.rot_brain = self.rot_brain.rotate_x(pi, point=self.axes.origin, inplace=False,
                                                   transform_all_input_vectors=True)

        # for rotation of sphere stim area
        if exec_show:
            self.stim_area = self.stim_area.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.stim_area = self.stim_area.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.stim_area = self.stim_area.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            if self.actor_sphere.GetVisibility():
                self.actor_sphere = self.p.add_mesh(self.stim_area, opacity=0.2, color='g', name="sphere_stim")
        else:
            self.stim_area = self.stim_area.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.stim_area = self.stim_area.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.stim_area = self.stim_area.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)

        # for rotation of ellipsoid stim area
        if exec_show:
            self.ellipsoid = self.ellipsoid.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.ellipsoid = self.ellipsoid.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.ellipsoid = self.ellipsoid.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            if self.actor_ellips.GetVisibility():
                self.actor_ellips = self.p.add_mesh(self.ellipsoid, opacity=0.2, color='b', name="eliips_stim")
        else:
            self.ellipsoid = self.ellipsoid.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.ellipsoid = self.ellipsoid.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.ellipsoid = self.ellipsoid.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)

        # for rotation of brain axis
        if exec_show:
            self.brain_xAx = self.brain_xAx.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_xAx = self.brain_xAx.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_xAx = self.brain_xAx.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)

            self.brain_yAx = self.brain_yAx.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_yAx = self.brain_yAx.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_yAx = self.brain_yAx.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)

            self.brain_zAx = self.brain_zAx.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_zAx = self.brain_zAx.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_zAx = self.brain_zAx.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            if self.brain_xAx_actor.GetVisibility():
                self.brain_xAx_actor = self.p.add_mesh(self.brain_xAx, color='r', name="brain_ax_x", line_width=2)
                self.brain_yAx_actor = self.p.add_mesh(self.brain_yAx, color='g', name="brain_ax_y", line_width=2)
                self.brain_zAx_actor = self.p.add_mesh(self.brain_zAx, color='b', name="brain_ax_z", line_width=2)

        else:
            self.brain_zAx = self.brain_zAx.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_zAx = self.brain_zAx.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_zAx = self.brain_zAx.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_yAx = self.brain_yAx.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_yAx = self.brain_yAx.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_yAx = self.brain_yAx.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_xAx = self.brain_xAx.rotate_z(ya, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_xAx = self.brain_xAx.rotate_y(ro, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)
            self.brain_xAx = self.brain_xAx.rotate_x(pi, point=self.axes.origin, inplace=True,
                                                     transform_all_input_vectors=True)

    def stim_point_move_callback(self, locs):
        self.xlabel1.setText("x= {:3.1f}mm".format(locs[0]))
        self.ylabel1.setText("y= {:.1f}mm".format(locs[1]))
        self.zlabel1.setText("z= {:.1f}mm".format(locs[2]))

        self.center_line = pv.Line((0, 0, 0),
                                   (locs[0] * stim_line_extension_scale, locs[1] * stim_line_extension_scale,
                                    locs[2] * stim_line_extension_scale))
        self.p.add_mesh(self.center_line, color='y', name="point_line", line_width=10)

        self.stimP_x = locs[0]
        self.stimP_y = locs[1]
        self.stimP_z = locs[2]

    def hide_stim_area(self):
        if self.bt_view_sphere.text() == "Show Sphere":
            self.actor_sphere.SetVisibility(True)
            self.actor_ellips.SetVisibility(False)
            self.bt_view_sphere.setText("Show Ellipsoid")
        elif self.bt_view_sphere.text() == "Show Ellipsoid":
            self.actor_sphere.SetVisibility(False)
            self.actor_ellips.SetVisibility(True)
            self.bt_view_sphere.setText("Show Stim Area")
        elif self.bt_view_sphere.text() == "Show Stim Area":
            self.actor_sphere.SetVisibility(True)
            self.actor_ellips.SetVisibility(True)
            self.bt_view_sphere.setText("Hide Stim Area")
        elif self.bt_view_sphere.text() == "Hide Stim Area":
            self.actor_sphere.SetVisibility(False)
            self.actor_ellips.SetVisibility(False)
            self.bt_view_sphere.setText("Show Sphere")

    def hide_head_brain(self):
        if self.bt_view_headbrain.text() == "Show Model":
            self.actor_head.SetVisibility(True)
            self.actor_brain.SetVisibility(True)
            self.bt_view_headbrain.setText("Show Brain")
        elif self.bt_view_headbrain.text() == "Show Brain":
            self.actor_head.SetVisibility(False)
            self.actor_brain.SetVisibility(True)
            self.bt_view_headbrain.setText("Show Head")
        elif self.bt_view_headbrain.text() == "Show Head":
            self.actor_head.SetVisibility(True)
            self.actor_brain.SetVisibility(False)
            self.bt_view_headbrain.setText("Hide Model")
        elif self.bt_view_headbrain.text() == "Hide Model":
            self.actor_head.SetVisibility(False)
            self.actor_brain.SetVisibility(False)
            self.bt_view_headbrain.setText("Show Model")

    def hide_axis_main(self):
        if self.bt_view_main_axis.isChecked():
            self.bt_view_main_axis.setText("Show Axis")
            self.axes_actor2.SetVisibility(False)
        else:
            self.bt_view_main_axis.setText("Hide Axis")
            self.axes_actor2.SetVisibility(True)

    def hide_axis_head(self, flag):
        self.brain_xAx_actor.SetVisibility(flag)
        self.brain_yAx_actor.SetVisibility(flag)
        self.brain_zAx_actor.SetVisibility(flag)

    def on_zoom_in(self):
        self.p.camera.zoom(1.5)

    def on_zoom_out(self):
        self.p.camera.zoom(0.5)

    def initiate_3d_modules(self):
        self.axes = pv.Axes(show_actor=True, actor_scale=200.0, line_width=5)
        self.axes.origin = (0, 0, 0)
        # axes.show_symmetric()
        # self.p.add_actor(axes.actor)

        self.axes_actor2 = self.p.add_axes_at_origin(xlabel='x', ylabel='y', zlabel='Z', line_width=3)
        self.axes_actor2.SetTotalLength(240, 240, 240)

        self.p.add_axes(interactive=None, line_width=2, color=None, x_color=None, y_color=None, z_color=None,
                        xlabel='X', ylabel='Y', zlabel='Z', labels_off=False, box=None, box_args=None,
                        viewport=(0, 0, 0.2, 0.2))

        # image = pv.read('head_roll.png')
        # self.p.add_mesh(image, rgb=True, cpos="xy")
        self.brain_xAx = pv.Line((-200, 0, 0), (200, 0, 0))
        self.brain_yAx = pv.Line((0, -200, 0), (0, 200, 0))
        self.brain_zAx = pv.Line((0, 0, -200), (0, 0, 200))
        self.brain_xAx_actor = self.p.add_mesh(self.brain_xAx, color='r', name="brain_ax_x", line_width=2)
        self.brain_yAx_actor = self.p.add_mesh(self.brain_yAx, color='g', name="brain_ax_y", line_width=2)
        self.brain_zAx_actor = self.p.add_mesh(self.brain_zAx, color='b', name="brain_ax_z", line_width=2)

        head_plane = pv.Plane([0, 0, -100], [0, 0, 1], 333, 333, 10, 10)
        # self.p.add_mesh(head_plane, color='#CE93D8')
        self.p.add_mesh(head_plane, color='#BDBDBD')

        body = pv.read(head_file_name)
        self.rot_body = body.translate([0, -60, 0])
        self.rot_body = self.rot_body.scale(head_stl_scale)
        # self.rot_body = self.rot_body.scale([1.3, 1.3, 0.7])
        self.rot_body = self.rot_body.rotate_z(180, point=self.axes.origin, inplace=False)
        self.rot_body = self.rot_body.translate([0, head_center_adjustment_y, 0])
        self.actor_head = self.p.add_mesh(self.rot_body, color=(158, 158, 158), specular=0.7,
                        specular_power=15, ambient=0.8, smooth_shading=True, opacity=headObj_opacity, name="rot_body")


        self.rot_brain = pv.read("../UI/STL/Brain for Half_Skull.stl")

        self.rot_brain = self.rot_brain.scale(1.13)
        self.rot_brain = self.rot_brain.rotate_z(90, point=self.axes.origin, inplace=False)
        self.rot_brain = self.rot_brain.translate([-1, -7, -30])
        self.actor_brain = self.p.add_mesh(self.rot_brain, color=(55, 55, 55), specular=0.7,
                        specular_power=15, ambient=0.8, smooth_shading=True, opacity=1, name="rot_brain")


        self.point1 = self.p.add_sphere_widget(callback=self.stim_point_move_callback, center=[0, 0, 0], radius=10,
                                               color="red")

        self.stim_area = pv.Sphere(radius=sphere_radius, start_phi=0, end_phi=180, start_theta=110, end_theta=250)
        self.stim_area = self.stim_area.rotate_y(90, point=self.axes.origin, inplace=False)
        # self.stim_area = self.stim_area.rotate_x(180, point=self.axes.origin, inplace=False)
        self.actor_sphere = self.p.add_mesh(self.stim_area, opacity=0.2, color='g', name="sphere_stim")

        self.ellipsoid = pv.ParametricEllipsoid(xradius=ellips_yradius, yradius=ellips_zradius,
                                                zradius=ellips_xradius, max_v=np.pi, min_u=np.radians(20),
                                                max_u=np.radians(160))
        self.ellipsoid = self.ellipsoid.rotate_z(90, point=self.axes.origin, inplace=False)
        self.ellipsoid = self.ellipsoid.rotate_y(90, point=self.axes.origin, inplace=False)
        self.actor_ellips = self.p.add_mesh(self.ellipsoid, opacity=0.2, color='b', name="eliips_stim")

        # self.p.add_background_image('aa3.png')

        self.p.add_ruler(
            pointa=[0, 0, 0],
            pointb=[0, 0, 180],
            flip_range=False,
            title="Z Distance",
        )
        self.p.enable_parallel_projection()

        self.p.camera_position = 'yz'
        self.p.camera.zoom(1.7)
        # self.p.camera.elevation -= 45

        self.p.show()


#######################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(1000, 700)
    window.move(450, 150)
    window.show()

    qm.apply_stylesheet(app, theme='dark_blue.xml')
    # print(qm.list_themes())
    app.exec()

