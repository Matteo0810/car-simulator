from math import cos, sin, pi

from helpers.vector import Vector3
from helpers.dotenv import get_env


class Camera:

    def __init__(self, coordinates: tuple = None, width: int = None, height: int = None):
        x, y, z = coordinates or (0, 0, 0)

        self._x = x
        self._y = y
        self._z = z
        self._width = width or get_env('WIDTH')
        self._height = height or get_env('HEIGHT')
        self._yaw = 0
        self._pitch = 0
        self._zoom = 0.3

    def move(self, dx, dy, dz):
        self._x += dx
        self._y += dy
        self._z += dz

    def set_width(self, width: int):
        self._width = width

    def set_height(self, height: int):
        self._height = height

    def set_zoom(self, zoom):
        self._zoom = zoom

    def set_direction(self, yaw, pitch):
        self._yaw = (yaw + 180) % 360 - 180
        self._pitch = max(-90, min(90, (pitch + 180) % 360 - 180))

    def set_position(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __iter__(self):
        return iter(self._get_data())

    def _get_data(self):
        return [self._x, self._y, self._z, (self._width, self._height)]

    def get_projection(self, obj: Vector3):
        X = obj.x
        Y = obj.y
        Z = obj.z

        n = self.direction * self.zoom * 1000
        C = self.position

        CA = Vector3(X, Y, Z) - C

        try:
            t = (n.x * (-n.x) + n.y * (-n.y) + n.z * (-n.z)) / (n.x * CA.x + n.y * CA.y + n.z * CA.z)

            CprimH = (t * CA - n)

            bx = CprimH.dot(self.right) + self._width / 2
            by = CprimH.dot(self.up) + self._height / 2

            return [int(bx),
                    int(by)]
        except ZeroDivisionError:
            return None

    def is_in_plan(self, obj):
        if type(obj) is list:
            return not (obj.x < 0 or obj.y < 0 or obj.x > self._width or obj.y > self._height)
        elif type(obj) is Vector3:
            return self.is_in_plan(self.get_projection(obj))

    @property
    def position(self):
        return Vector3(self._x, self._y, self._z)

    @property
    def zoom(self):
        return self._zoom

    @property
    def direction(self):
        xy = cos(-self.pitch * pi / 180)
        x = -xy * sin(self.yaw * pi / 180)
        y = xy * cos(self.yaw * pi / 180)
        z = sin(self.pitch * pi / 180)
        return Vector3(x, y, z)

    @property
    def up(self):
        xy = cos(-(self.pitch + 90) * pi / 180)
        x = -xy * sin(self.yaw * pi / 180)
        y = xy * cos(self.yaw * pi / 180)
        z = sin((self.pitch + 90) * pi / 180)
        return Vector3(x, y, z)

    @property
    def right(self):
        return self.direction.cross(self.up)

    @property
    def yaw(self):
        return self._yaw

    @property
    def pitch(self):
        return self._pitch
