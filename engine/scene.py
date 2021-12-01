from tkinter import Canvas

from engine.objloader import ObjLoader
from engine.polygon.polygon import Polygon
from engine.camera import Camera
from engine.controller import Controller

from helpers.dotenv import get_env


class Scene(Canvas):

    def __init__(self, root):
        super().__init__(
            master=root,
            height=get_env('HEIGHT'),
            width=get_env('WIDTH'),
            bg="black"
        )

        # models 3d
        self._objects: dict[int, Polygon] = dict()
        self._obj_id = 1

        # cameras
        self._cameras: dict[int, Camera] = dict()
        self._cam_id = 1

        # camera par défaut
        self._default_camera = self.add_camera()

        # mode développeur
        self._is_dev_env()

    def _is_dev_env(self):
        if get_env('ENV') == 'DEV':
            Controller(self).handle()

    def add_obj(self, path: str) -> Polygon:
        obj = ObjLoader.load(path)
        polygon = obj.get_polygon()
        self._objects[self._obj_id] = polygon
        self._obj_id += 1
        return polygon

    def get_obj(self, object_id: int) -> Polygon:
        if object_id in self._objects:
            return self._objects[object_id]
        raise ValueError('Objet introuvable')

    def add_camera(self) -> Camera:
        camera = Camera()
        self._cameras[self._cam_id] = camera
        self._cam_id += 1
        return camera

    def get_camera(self, camera_id: int) -> Camera:
        if camera_id in self._cameras:
            return self._cameras[camera_id]
        raise ValueError('Camera introuvable')

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
