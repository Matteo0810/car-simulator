from tkinter import Canvas

from engine.scene.models import Models
from engine.scene.camera import Camera
from engine.scene.controller import Controller

from helpers.dotenv import get_env


class Scene(Canvas):

    def __init__(self, root):
        super().__init__(
            master=root,
            height=get_env('HEIGHT'),
            width=get_env('WIDTH'),
            bg="black"
        )

        self._models = Models()

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

    def add_camera(self) -> Camera:
        camera = Camera()
        self._cameras[self._cam_id] = camera
        self._cam_id += 1
        return camera

    def get_camera(self, camera_id: int) -> Camera:
        if camera_id in self._cameras:
            return self._cameras[camera_id]
        raise ValueError('Camera introuvable')

    def get_models(self) -> Models:
        return self._models

    def clear(self):
        self.delete('all')

    def update(self):
        self.clear()
        self._render()

    def show(self):
        self._render()
        self.pack()

    def _render(self):
        for polygon in self._models.all():
            polygon.render(self)
