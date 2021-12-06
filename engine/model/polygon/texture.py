class Texture:

    def __init__(self, uv: list):
        self._u = 0
        self._v = 0
        self._average = (self._u+self._v)/2

    def get_alpha(self):
        return self._average

    def __str__(self):
        return f'UV ({self._u}, {self._v})'
