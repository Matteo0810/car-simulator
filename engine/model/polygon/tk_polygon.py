from tkinter import Canvas


class TkPolygon:
    def __init__(self, points, fill):
        self._points = points
        self._fill = fill
    
    def draw(self, canvas: Canvas):
        return canvas.create_polygon(self._points, fill=self._fill)
