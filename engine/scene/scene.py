from tkinter import ANCHOR, Canvas, Label, Button, PhotoImage
from time import time
from threading import Thread

from helpers.dotenv import get_env

from engine.scene.models import Models
from engine.scene.camera import Camera


class Scene(Canvas):
    
    def __init__(self, root, is_loading=False):
        super().__init__(
            master=root,
            height=get_env('HEIGHT'),
            width=get_env('WIDTH'),
            bg="black"
        )
        
        self.gui = root
        self.width = get_env('WIDTH')
        self.height = get_env('HEIGHT')
        
        self.mid_width = self.width // 2
        self.mid_height = self.height // 2
        
        self._default_camera = Camera()

        self._is_loading = is_loading
        self._loading_thread = None

        self._models = Models(self._default_camera, None)
        
        if self.is_dev:
            self._fps = _FPS(self)
            self._fps.update()

    def get_camera(self) -> Camera:
        return self._default_camera
    
    def get_models(self) -> Models:
        return self._models
    
    def update(self, callback=None):
        self.clear()
        self._models.update(self, callback)
        
        if self.is_dev:
            self._fps.update()
    
    def clear(self):
        self.delete('all')
    
    def show(self):
        if self._is_loading:
            self.pack()
            return
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
        
        # default events
        button.bind("<Enter>", func=lambda _: button.config(text='> ' + current_text))
        button.bind("<Leave>", func=lambda _: button.config(text=current_text))
        
        button.place(x=x, y=y)
        return button

    @property
    def is_dev(self):
        return get_env('ENV') == 'DEV'


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
