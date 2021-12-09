from tkinter import Canvas, Label

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
            bg="black",
        )

        self._models = Models()

        self._cameras: dict[int, Camera] = dict()
        self._cam_id = 1
        self._default_camera = self.add_camera()

        # FPS (Mode dev seulement)
        self._fps_label = None
        self._update_fps()

        if self._dev_env():
            self._controller = Controller(self).setup()

    def _dev_env(self):
        return get_env('ENV') == 'DEV'

    def get_controller(self):
        if get_env('ENV') == 'DEV':
            return self._controller

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

    def update(self, callback = None):
        self.clear()
        self._models.update(self, callback)

        if self._dev_env():
            self._update_fps()

    def _update_fps(self):
        # TODO FPS à fix...
        if self._fps_label is not None:
            self._fps_label['text'] = f'FPS: 0'
            return
        self._fps_label = self.add_label((get_env('WIDTH') // 2, 15), f'FPS: 0')

    def clear(self):
        self.delete('all')

    def show(self):
        self._models.update(self)
        self.pack()

    def add_label(self, coordinates: tuple, text: str, font_size: int = 15):
        x, y = coordinates
        label = Label(self,
                      text=text,
                      background="black",
                      foreground="white",
                      font=("impact", font_size))
        label.place(x=x, y=y)
        return label