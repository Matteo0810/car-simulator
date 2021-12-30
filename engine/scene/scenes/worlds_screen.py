from engine.scene.scene import Scene


class WorldsScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.add_label((self.middle_width - 50, 200), "Mondes", 25)

        self.add_button((self.middle_width - 30, 260), "Retour", self.gui.back_scene, 20)
