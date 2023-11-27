import numpy as np
from pyvista import QtInteractor
from trimesh import transformations


class MyClass:
    def __init__(self, frame, pv=None):


        new_position = [-20, 90, 0]  # مختصات جدید موقعیت کویل را وارد کنید
        transform = np.eye(4)
        transform[:3, 3] = new_position
        mesh_coil.transform(transform)


        rotation_angle_degrees = 30
        rotation_axis = [0, 1, 0]  # محور y
        rotation_angle_radians = np.radians(rotation_angle_degrees)
        rotation_matrix = transformations.rotation_matrix(rotation_angle_radians, rotation_axis)
        mesh_coil.transform(rotation_matrix)

        rotation_angle_degrees = 70
        rotation_axis = [1, 0, 0]  # محور X
        rotation_angle_radians = np.radians(rotation_angle_degrees)
        rotation_matrix = transformations.rotation_matrix(rotation_angle_radians, rotation_axis)
        mesh_coil.transform(rotation_matrix)

        rotation_angle_degrees = 360
        rotation_axis = [0, 0, 1]  # محور Z
        rotation_angle_radians = np.radians(rotation_angle_degrees)
        rotation_matrix = transformations.rotation_matrix(rotation_angle_radians, rotation_axis)
        mesh_coil.transform(rotation_matrix)



