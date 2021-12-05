from helpers.utils import *


class Camera2d:
    def __init__(self, x, y, zoom=1):
        self._x = x
        self._y = y
        self._zoom = zoom
    
    x = property_get("x")
    y = property_get("y")
    zoom = property_get("zoom")
    
    def move_to(self, x, y):
        self._x = x
        self._y = y
