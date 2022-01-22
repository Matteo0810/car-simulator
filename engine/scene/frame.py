from tkinter import Tk, PhotoImage

from helpers.dotenv import get_env
from helpers.utils import get_path
from engine.scene.scenes.before_title_screen import BeforeTitleScreen


class Frame(Tk):

    def __init__(self):
        super().__init__()

        # settings
        WIDTH, HEIGHT = get_env('WIDTH'), get_env('HEIGHT')
        self.title('Car simulator')
        self.iconphoto(False, PhotoImage(file=get_path('assets/images/icon.png')))
        self.geometry(f'{WIDTH}x{HEIGHT}')
        self.resizable(False, False)

        self._scene = BeforeTitleScreen(self)
        self._previous_scene = None

    def use(self, scene):
        self._previous_scene = self._scene.__class__
        self._scene.destroy()
        self._scene = scene(self)
        self._scene.show()

    def previous_scene(self):
        self.use(self._previous_scene)

    def get_scene(self):
        return self._scene

    def get_models(self):
        return self._scene.get_models()

    def show(self):
        self._scene.show()
        self.mainloop()
