from math import pi, cos, sin
from helpers.dotenv import get_env


class Vertex:

    def __init__(self, coordinates: list, texture: int = 0):
        x, y, z = coordinates
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)

        self._texture = texture

        self._size = (get_env('WIDTH'), get_env('HEIGHT'))
        self._distance = get_env('DISTANCE')
        self._scale = get_env('SCALE')

    def rotate(self, axis: str, angle: float):
        angle = angle / 450 * 180 / pi

        if axis == 'z':
            self._x = self._x * cos(angle) - self._y * sin(angle)
            self._y = self._y * cos(angle) + self._x * sin(angle)
        elif axis == 'x':
            self._y = self._y * cos(angle) - self._z * sin(angle)
            self._z = self._z * cos(angle) + self._y * sin(angle)
        elif axis == 'y':
            self._x = self._x * cos(angle) - self._z * sin(angle)
            self._z = self._z * cos(angle) + self._x * sin(angle)
        else:
            raise ValueError('Axe invalide')

    def move(self, axis: str, newPos: float):
        try:
            self.__setattr__(f'_{axis}', newPos)
        except ValueError:
            raise ValueError('Axe invalide')

    def set_texture(self, texture):
        self._texture = texture

    def to_2d(self) -> list:
        width, height = self._size
        return [int(width / 2 + ((self._x * self._distance) / (self._z + self._distance)) * self._scale),
                int(height / 2 + ((self._y * self._distance) / (self._z + self._distance)) * self._scale)]

    def get_texture(self):
        return self._texture

    def __iter__(self):
        return iter([self._x, self._y, self._z])

    def __tuple__(self):
        return self.flat()

    def __str__(self):
        return f'3d Coordinates ({self._x}, {self._y}, {self._z})'
