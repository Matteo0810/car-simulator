from math import pi, cos, sin

from helpers.vector import Vector3


class Vertex:

    def __init__(self, coordinates: Vector3, obj_pos: Vector3):
        self._x, self._y, self._z = tuple(coordinates)
        self._obj_pos = obj_pos
        
        self._rotations = {'x': 0, 'y': 0, 'z': 0}

    def rotate(self, axis: str, angle: float):
        angle *= pi / 180

        if axis == 'z' or axis == 'x' or axis == 'y':
            self._rotations[axis] += angle
        else:
            raise ValueError('Axe invalide')

    def set_rotation(self, axis: str, angle: float):
        angle *= pi / 180

        if axis == 'z' or axis == 'x' or axis == 'y':
            self._rotations[axis] = angle
        else:
            raise ValueError('Axe invalide')

    def move(self, dx, dy, dz):
        self._obj_pos += Vector3(dx, dy, dz)
    
    def set_obj_pos(self, x, y, z):
        self._obj_pos = Vector3(x, y, z)

    def to_2d(self, camera) -> list:
        return camera.get_projection(self.position)
    
    @property
    def position(self):
        x = self._x
        y = self._y
        z = self._z
        for axis, angle in self._rotations.items():
            if axis == 'z':
                X = x * cos(angle) - y * sin(angle)
                Y = y * cos(angle) + x * sin(angle)
                Z = z
            elif axis == 'x':
                Y = y * cos(angle) - z * sin(angle)
                Z = z * cos(angle) + y * sin(angle)
                X = x
            elif axis == 'y':
                X = x * cos(angle) - z * sin(angle)
                Z = z * cos(angle) + x * sin(angle)
                Y = y
            
            x = X
            y = Y
            z = Z

        X = x + self._obj_pos.x
        Y = y + self._obj_pos.y
        Z = z + self._obj_pos.z
        return Vector3(X, Y, Z)
    
    def plan_distance(self, camera):
        return camera.direction.dot(self.position - camera.position)

    def __str__(self):
        return f'3d Coordinates ({self._x}, {self._y}, {self._z})'
