from engine.scene.scene import Scene
from helpers.dotenv import get_env


class CreditsScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        height = self.mid_height
        for credit in open(f'{get_env("ASSETS_DIR")}credits.txt', 'r', encoding="utf-8").readlines():
            height += 40
            label = self.add_label((self.mid_width - 100 - ((0, 20)[credit.startswith('-')]), height),
                                   credit.replace('-', ''), ((16, 20)[credit.startswith('-')]))
            self.up(label, height)

    def up(self, label, height):
        if height >= -100:
            new_height = height - 1
            label.place(y=new_height)
            self.gui.after(25, lambda: self.up(label, new_height))
