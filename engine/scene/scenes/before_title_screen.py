from helpers.color import Color

from engine.scene.scene import Scene


class BeforeTitleScreen(Scene):

    def __init__(self, root):
        super().__init__(root)
        self._fade_title(self.add_label((self.mid_width - 200, self.mid_height - 50), "NSI PRODUCTION", 40))
        self._fade_title(self.add_label((self.mid_width - 100, self.mid_height + 10), "Presente", 30))

    def _fade_title(self, label, rgb=(255, 255, 255)):
        r, g, b = rgb
        if r + g + b == 0:
            return self.gui.use(self.gui.screens['title'])
        label['fg'] = Color(r, g, b, 1)
        self.gui.after(15, lambda: self._fade_title(label, (r - 5, g - 5, b - 5)))
