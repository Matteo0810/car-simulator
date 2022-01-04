from helpers.color import Color

from engine.scene.scene import Scene
from engine.scene.scenes.title_screen import TitleScreen


class BeforeTitleScreen(Scene):

    def __init__(self, root):
        super().__init__(root)
        self._fade_title(self.add_label((self.mid_width-200, self.mid_height-50), "NSI PRODUCTION", 40))


    def _fade_title(self, label, rgb = (255, 255, 255)):
        r,g,b = rgb
        if r+g+b == 0:
            return self.gui.use(TitleScreen)
        label['fg'] = Color(r, g, b, 1)
        self.gui.after(15, lambda: self._fade_title(label, (r-5, g-5, b-5)))