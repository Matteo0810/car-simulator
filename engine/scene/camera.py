from math import sqrt

from helpers.vector import Vector3
from helpers.dotenv import get_env


class Camera:

    def __init__(self, coordinates: tuple = None, width: int = None, height: int = None):
        x, y, z = coordinates or (0, 0, 0)

        self._x = x
        self._y = y
        self._z = z
        self._angle = 0
        self._width = width or get_env('WIDTH')
        self._height = height or get_env('HEIGHT')
        self._direction = Vector3(0, 0, 0)

    def move(self, dx, dy, dz):
        self._x += dx
        self._y += dy
        self._z += dz

    def set_width(self, width: int):
        self._width = width

    def set_height(self, height: int):
        self._height = height

    def get_direction(self):
        return self._direction

    def set_direction(self, x, y, z):
        self._direction = Vector3(x, y, z)

    def get_distance_from(self, obj) -> float:
        x, y, z = list(obj)
        return sqrt((x - self._x) ** 2 + (y - self._y) ** 2 + (z - self._z) ** 2)

    def __iter__(self):
        return iter(self._get_data())

    def __tuple__(self):
        return map(str, self._get_data())

    def _get_data(self):
        return [self._x, self._y, self._z, self._angle, (self._width, self._height)]

    @property
    def position(self):
        return Vector3(self._x, self._y, self._z)
