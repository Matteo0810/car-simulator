from engine.scene.scene import Scene
from engine.scene.scenes.world_screen import WorldScreen


class WorldsScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.add_label((self.mid_width - 50, 200), "Mondes", 25)

        self.add_button((self.mid_width - 30, 260), "World test", lambda: self.gui.use(WorldScreen), 20)
        self.add_button((self.mid_width - 30, 310), "Retour", self.gui.previous_scene, 20)
