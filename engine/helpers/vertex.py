from math import pi, cos, sin


class Vertex:

    def __init__(self, x: int, y: int, z: int, texture: int = 0, props: tuple = None):
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)
        self._texture = texture
        self._props = props

    def rotate(self, axis: str, angle: float):
        angle = angle / 450 * 180 / pi

        if axis == 'x':
            self._y = self._y * cos(angle) - self._y * sin(angle)
            self._z = self._z * cos(angle) + self._z * sin(angle)
        elif axis == 'y':
            self._x = self._x * cos(angle) - self._x * sin(angle)
            self._z = self._z * cos(angle) + self._z * sin(angle)
        elif axis == 'z':
            self._x = self._x * cos(angle) - self._x * sin(angle)
            self._y = self._y * cos(angle) + self._y * sin(angle)
        else:
            raise ValueError('Axe invalide')

    def move(self, axis: str, newPos: float):
        try:
            self.__setattr__(f'_{axis}', newPos)
        except ValueError:
            raise ValueError('Axe invalide')

    def set_texture(self, texture):
        self._texture = texture

    def to_2d(self):
        size, distance, scale = self._props
        width, height = size
        return int(width / 2 + ((self._x * distance) / (self._z + distance)) * scale), \
               int(height / 2 + ((self._y * distance) / (self._z + distance)) * scale)

    def get_texture(self):
        return self._texture

    def __iter__(self):
        return iter([self._x, self._y, self._z])

    def __tuple__(self):
        return map(str, [self._x, self._y, self._z])

    def __str__(self):
        return f'3d Coordinates ({self._x}, {self._y}, {self._z})'
