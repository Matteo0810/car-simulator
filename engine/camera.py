from math import sqrt
from helpers.dotenv import get_env


class Camera:

    def __init__(self, x=0, y=0, z=0):
        self._x = x
        self._y = y
        self._z = z
        self._width = get_env('WIDTH')
        self._height = get_env('HEIGHT')

    def move(self, axis: str, newPos: float):
        try:
            self.__setattr__(f'_{axis}', newPos)
        except ValueError:
            raise ValueError('Axe invalide')

    def get_distance_from(self, obj) -> float:
        x, y, z = tuple(obj)
        return sqrt((x - self._x) ** 2 + (y - self._y) ** 2 + (z - self._z) ** 2)
