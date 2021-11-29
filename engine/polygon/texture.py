class Texture:

    def __init__(self, uv: list):
        u, v = uv
        self._u = float(u)
        self._v = float(v)
        self._average = (self._u+self._v)/2

    def get_alpha(self):
        return self._average

    def __str__(self):
        return f'UV ({self._u}, {self._v})'
