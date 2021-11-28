from .vertex import Vertex


class Face:

    def __init__(self, a: Vertex, b: Vertex, c: Vertex):
        self._a = a
        self._b = b
        self._c = c

    def create(self, canvas):
        canvas.create_polygon(
            list(sum((self._a.to_2d(), self._b.to_2d(), self._c.to_2d()), ())),
            fill="",
            outline="gray"
        )
