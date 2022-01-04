from engine.scene.scene import Scene


class CreditsScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.create_rectangle(
            self.width, 0,
            self.width, self.height, 
            fill="black")
        self.add_label((self.mid_width - 60, 200), "Crédits", 25)

        line = self.mid_height-100
        credits = self._get_credits()
        for credit in credits:
            line += 40
            self.add_label((self.mid_width - 100 - ((0, 20)[credit.startswith('-')]), line),
                credit.replace('-', ''), ((16, 20)[credit.startswith('-')]))    


    def _get_credits(self):
        return open('world/assets/credits.txt', 'r', encoding="utf-8").readlines()