from math import sqrt
from helpers.dotenv import get_env


class Camera:

    def __init__(self, coordinates: tuple, width: int = get_env('WIDTH'), height: int = get_env('HEIGHT')):
        x, y, z = coordinates

        self._x = x
        self._y = y
        self._z = z
        self._width = width
        self._height = height

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

    def get_distance_from(self, obj) -> float:
        x, y, z = list(obj)
        return sqrt((x - self._x) ** 2 + (y - self._y) ** 2 + (z - self._z) ** 2)
