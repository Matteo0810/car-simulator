from .vertex import Vertex


class Face:

    def __init__(self, a: Vertex, b: Vertex, c: Vertex):
        self._a = a
        self._b = b
        self._c = c

    def get_a(self):
        return self._a

    def get_b(self):
        return self._b

    def get_c(self):
        return self._c

    def create(self, canvas):
        canvas.create_polygon(
            self._a.to_2d() + self._b.to_2d() + self._c.to_2d(),
            outline="gray"
        )