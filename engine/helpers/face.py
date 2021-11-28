from .vertex import Vertex
from random import randint
from .color import Color


class Face:

    def __init__(self, a: Vertex, b: Vertex, c: Vertex):
        self._a = a
        self._b = b
        self._c = c

    """
    def _get_UV(self):
        return sum(list(sum((
            self._a.get_texture(),
            self._b.get_texture(),
            self._c.get_texture()),
            ()))) / 3
    """

    def get_a(self):
        return self._a

    def get_b(self):
        return self._b

    def get_c(self):
        return self._c

    def create(self, canvas):
        canvas.create_polygon(
            list(sum((
                self._a.to_2d(),
                self._b.to_2d(),
                self._c.to_2d()),
                ())),
            outline="gray"
        )