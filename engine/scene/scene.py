import json

from tkinter import Canvas, Label, Button
from time import time
from helpers.dotenv import get_env

from engine.scene.models import Models
from engine.scene.camera import Camera
from engine.scene.controller import Controller


class Scene(Canvas):

    def __init__(self, root, controller=False, loaded_content=None):
        super().__init__(
            master=root,
            height=get_env('HEIGHT'),
            width=get_env('WIDTH'),
            bg="black"
        )

        self.gui = root
        self.width = get_env('WIDTH')
        self.height = get_env('HEIGHT')

        self._default_camera = Camera()
        self._models = Models(self._default_camera, None)

        if self._dev():
            self._fps = _FPS(self)
            self._fps.update()

            if controller:
                self._controller = Controller(self).setup()

    def _dev(self):
        return get_env('ENV') == 'DEV'

    def get_controller(self):
        if self._dev():
            return self._controller

    def get_camera(self) -> Camera:
        return self._default_camera

    def get_models(self) -> Models:
        return self._models

    def update(self, callback=None):
        self.clear()
        self._models.update(self, callback)

        if self._dev():
            self._fps.update()

    def clear(self):
        self.delete('all')

    def show(self):
        self._models.update(self)
        self.pack()

    def add_label(self, coordinates: tuple, text: str, font_size: int = 16, color: str = "white"):
        x, y = coordinates
        label = Label(self,
                      text=text,
                      background="black",
                      foreground=color,
                      font=("fixedsys", font_size))
        label.place(x=x, y=y)
        return label

    def add_button(self, coordinates: tuple, text: str, callback, font_size: int = 16, color: str = "white"):
        x, y = coordinates
        button = Button(self,
                        text=text,
                        activebackground="black",
                        border=0,
                        relief='flat',
                        background="black",
                        foreground=color,
                        activeforeground=color,
                        command=callback,
                        font=("fixedsys", font_size))

        current_text = button.cget("text")

        # events
        button.bind("<Enter>", func=lambda _: button.config(text='> ' + current_text))
        button.bind("<Leave>", func=lambda _: button.config(text=current_text))
        button.place(x=x, y=y)
        return button


class _FPS:

    def __init__(self, scene):
        self._scene = scene
        self._count = 0
        self._last = time()
        self._label = None

    def _update_count(self):
        current = time()
        if (current - self._last) > 1:
            self._count = 0
            self._last = current
            return
        self._count += 1

    def update(self):
        self._update_count()
        if self._label is not None:
            self._label['text'] = f'[Dev] FPS: {self._count}'
            return
        self._label = self._scene.add_label((get_env('WIDTH') // 2, 15), f'[Dev] FPS: 0')


class _Loader:

    def __init__(self, scene):
        self._scene = scene
        self._label = None
        self._progress_bar = None
        self._progress = 0
        self._max = 100

    def progress(self):
        if self._max > self._progress:
            self._progress += 2
            self._update_progress()

    def _update_progress(self):
        scene = self._scene
        coords = scene.coords(self._progress_bar)
        coords[2] += self._progress
        scene.coords(self._progress_bar, *coords)

    def delete(self):
        scene = self._scene
        scene.delete(self._progress_bar)
        self._label.destroy()

    def load(self):
        if not self._label and not self._progress_bar:
            m_width, m_height = get_env('WIDTH') // 2, get_env('HEIGHT') // 2
            self._label = self._scene.add_label((m_width - 60, m_height), f'Chargement en cours...')
            self._progress_bar = self._scene.create_rectangle(m_width, m_height, m_width + self._progress,
                                                              m_height + 70, fill="white")
        return self
