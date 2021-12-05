

class Camera2d:
    def __init__(self, x, y, zoom=1):
        self._x = x
        self._y = y
        self._zoom = zoom
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def zoom(self):
        return self._zoom
    
    def move_to(self, x, y):
        self._x = x
        self._y = y
