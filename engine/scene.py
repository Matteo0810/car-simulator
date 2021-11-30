from tkinter import Canvas

from engine.objloader import ObjLoader
from engine.polygon.polygon import Polygon
from helpers.dotenv import get_env


class Scene(Canvas):

    def __init__(self, root):
        super().__init__(
            master=root,
            height=get_env('HEIGHT'),
            width=get_env('WIDTH'),
            bg="black"
        )

        self._objects: dict[int, Polygon] = dict()
        self._id = 1
        self._previous = []

        self.bind('<B1-Motion>', self._rotate)
        self.bind('<ButtonRelease-1>', self._reset_rotate)

    def _reset_rotate(self, _):
        self._previous = []

    def _rotate(self, event):
        if self._previous:
            self._objects[1].rotate('x', (event.y - self._previous[1]) / 20)
            self._objects[1].rotate('y', (event.x - self._previous[0]) / 20)
            self.update()
        self._previous = [event.x, event.y]

    def add_obj(self, path: str) -> Polygon:
        obj = ObjLoader.load(path)
        polygon = obj.get_polygon()
        self._objects[self._id] = polygon
        self._id += 1
        return polygon

    def get_obj(self, object_id: int) -> Polygon:
        if object_id in self._objects:
            return self._objects[object_id]
        raise ValueError('Objet introuvable')

    def clear(self):
        self.delete('all')

    def update(self):
        self.clear()
        self._render()

    def show(self):
        self._render()
        self.pack()

    def _render(self):
        for polygon in self._objects.values():
            polygon.render(self)
