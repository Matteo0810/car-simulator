from engine.scene.scene import Scene


class SettingsScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.add_label((self.middle_width - 60, 200), "Options", 25)
        self.add_button((self.middle_width - 30, 260), "Musique", None, 20)
        self.add_button((self.middle_width - 30, 310), "Retour", self.gui.back_scene, 20)
