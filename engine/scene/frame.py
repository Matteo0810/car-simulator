from tkinter import Tk, PhotoImage

from helpers.dotenv import get_env
from helpers.utils import get_path

from engine.scene.scenes.before_title_screen import BeforeTitleScreen
from engine.scene.scenes.title_screen import TitleScreen
from engine.scene.scenes.worlds_screen import WorldsScreen
from engine.scene.scenes.credits_screen import CreditsScreen


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
        self._last_scene = None
        
        import main
        self.after(1000, main.start_music)

    screens = {
        "title": TitleScreen,
        "worlds": WorldsScreen,
        "credits": CreditsScreen
    }

    def use(self, screen):
        self._last_scene = self._scene.__class__
        self._scene.events.emit('leave')
        self._scene.destroy()
        self._scene = screen(self)
        self._scene.show()

    def use_last_scene(self):
        self.use(self._last_scene)

    def show(self):
        self._scene.show()
        self.mainloop()
