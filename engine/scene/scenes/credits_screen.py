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
        height += 40 * 15

        quit_button = self.add_button((self.mid_width - 100, height), "Retour au menu", self.gui.use_last_scene)
        self.up(quit_button, height, min_height=get_env("HEIGHT") - 40)

    def up(self, label, height, min_height=-100):
        if height >= min_height:
            new_height = height - 1
            label.place(y=new_height)
            self.gui.after(25, lambda: self.up(label, new_height, min_height))
