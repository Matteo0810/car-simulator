from engine.scene.scene import Scene


class CreditsScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        height = self.mid_height
        for credit in self._get_credits():
            height += 40
            label = self.add_label((self.mid_width - 100 - ((0, 20)[credit.startswith('-')]), height),
                                   credit.replace('-', ''), ((16, 20)[credit.startswith('-')]))
            self.up(label, height)

    def _get_credits(self):
        return open('world/assets/credits.txt', 'r', encoding="utf-8").readlines()

    def up(self, label, height):
        if height >= -100:
            new_height = height - 10
            label.place(y=new_height)
            self.gui.after(25, lambda: self.up(label, new_height))
