class Color:

    def __init__(self, r: int, g: int, b: int, alpha: float = 0):
        self._r = round(r * alpha + (1.0 - alpha) * 255)
        self._g = round(g * alpha + (1.0 - alpha) * 255)
        self._b = round(b * alpha + (1.0 - alpha) * 255)

    @staticmethod
    def from_list(rgba: list):
        r, g, b, a = rgba
        return Color(r, g, b, a)

    def __iter__(self):
        return [self._r, self._g, self._b].__iter__()

    def __str__(self):
        return "#%02x%02x%02x" % (self._r, self._g, self._b)