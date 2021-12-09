from math import sqrt
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

    def move(self, axis: str, newPos: float):
        try:
            var_name = f'_{axis}'
            self.__setattr__(var_name, self.__getattribute__(var_name) + newPos)
        except ValueError:
            raise ValueError('Axe invalide')

    def set_width(self, width: int):
        self._width = width

    def set_height(self, height: int):
        self._height = height

    def __iter__(self):
        return iter(self._get_data())

    def __tuple(self):
        return map(str, self._get_data())

    def get_distance_from(self, obj) -> float:
        x, y, z = list(obj)
        return sqrt((x - self._x) ** 2 + (y - self._y) ** 2 + (z - self._z) ** 2)

    def _get_data(self):
        return [self._x, self._y, self._z, self._angle, (self._width, self._height)]
