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
        for value in self._objects.values():
            value.get_polygon().render(self)
