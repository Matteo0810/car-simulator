from tkinter import Canvas, Label, Button

from helpers.event_emitter import EventEmitter
from helpers.dotenv import get_env

from engine.scene.tools.models import Models
from engine.scene.tools.camera import Camera
from engine.scene.tools.fps import FPS


class Scene(Canvas):
    
    def __init__(self, root, title=None):
        super().__init__(
            master=root,
            height=get_env('HEIGHT'),
            width=get_env('WIDTH'),
            bg="black"
        )

        self.gui = root
        self.events = EventEmitter()

        self._buttons = []
        self._title = title

        self.width = get_env('WIDTH')
        self.height = get_env('HEIGHT')
        
        self.mid_width = self.width // 2
        self.mid_height = self.height // 2
        
        self._default_camera = Camera()

        self._models = Models(self._default_camera)
        
        if self.is_dev:
            self._fps = FPS(self)
            self._fps.update()

    def set_buttons(self, buttons):
        self._buttons = buttons

    def get_camera(self) -> Camera:
        return self._default_camera
    
    def get_models(self) -> Models:
        return self._models
    
    def update(self):
        self.clear()

        faces = []
        for polygon in self.get_models().all():
            faces.extend(polygon.faces)

        for face in sorted(faces, key=lambda f: f.avg_dist()):
            face.create(self)
        
        if self.is_dev:
            self._fps.update()
    
    def clear(self):
        self.delete('all')
    
    def show(self):
        if self._title:
            self.add_label((self.mid_width - 100, 200), self._title, 25)
        for button, i in zip(self._buttons, range(len(self._buttons))):
            self.add_button((self.mid_width - 30, 260 + 49 * i), text=button['text'],
                            callback=button['callback'], font_size=20)

        self.update()
        self.place(x=-2, y=-2)

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
