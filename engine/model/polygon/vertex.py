from math import pi, cos, sin

from helpers.dotenv import get_env
from helpers.vector import Vector3


class Vertex:

    def __init__(self, coordinates: Vector3, obj_pos: Vector3, distance: int = 6):
        self._x, self._y, self._z = tuple(coordinates)
        self._obj_pos = obj_pos

        self._distance = distance

    def rotate(self, axis: str, angle: float):
        angle *= pi / 180

        if axis == 'z':
            x = self._x * cos(angle) - self._y * sin(angle)
            y = self._y * cos(angle) + self._x * sin(angle)
            z = self._z
        elif axis == 'x':
            y = self._y * cos(angle) - self._z * sin(angle)
            z = self._z * cos(angle) + self._y * sin(angle)
            x = self._x
        elif axis == 'y':
            x = self._x * cos(angle) - self._z * sin(angle)
            z = self._z * cos(angle) + self._x * sin(angle)
            y = self._y
        else:
            raise ValueError('Axe invalide')

        self._x = x
        self._y = y
        self._z = z

    def move(self, axis: str, newPos: float):
        try:
            var_name = f'_{axis}'
            self.__setattr__(var_name, self.__getattribute__(var_name) + newPos)
        except ValueError:
            raise ValueError('Axe invalide')
 
    def rescale(self, scale: int):
        self._scale = scale

    def to_2d(self, camera) -> list:
        X = self._x + self._obj_pos.x
        Y = self._y + self._obj_pos.y
        Z = self._z + self._obj_pos.z
        
        n = -camera.direction * camera.zoom * 1000
        C = camera.position
        
        CA = Vector3(X, Y, Z) - C

        try:
            t = (n.x * (-n.x) + n.y * (-n.y) + n.z * (-n.z)) / (n.x * CA.x + n.y * CA.y + n.z * CA.z)
            
            CprimH = (t * CA - n)
            
            bx = CprimH.dot(camera.right) + get_env('WIDTH') / 2
            by = -CprimH.dot(camera.up) + get_env('HEIGHT') / 2
            
            return [int(bx),
                    int(by)]
        except ZeroDivisionError:
            return [1000, 1000]
    
    @property
    def position(self):
        return Vector3(self._x + self._obj_pos.x, self._y + self._obj_pos.y, self._z + self._obj_pos.z)
    
    def plan_distance(self, camera):
        return camera.direction.dot(self.position - camera.position)

    def __iter__(self):
        return [self._x, self._y, self._z].__iter__()

    def __str__(self):
        return f'3d Coordinates ({self._x}, {self._y}, {self._z})'
