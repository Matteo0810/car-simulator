from engine.scene.scene import Scene

from engine.scene.scenes.credits_screen import CreditsScreen
from engine.scene.scenes.settings_screen import SettingsScreen
from engine.scene.scenes.worlds_screen import WorldsScreen
from helpers.vector import Vector3


class TitleScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.add_label((self.mid_width - 130, 200), "Car simulator", 25)

        models = self.get_models()
        
        self.get_camera().set_direction(0, 0)
        self.get_camera().set_position(0, 0, 0)
        car = models.add('car/car', position=Vector3(-2.8, 10, -2.7))
        car.rotate('x', -90).rotate('y', 0).rotate('z', 30)

        self.add_button((self.mid_width - 30, 260), "Mondes", lambda: self.gui.use(WorldsScreen), 20)
        self.add_button((self.mid_width - 30, 310), "Options", lambda: self.gui.use(SettingsScreen), 20)
        self.add_button((self.mid_width - 30, 360), "Crédits", lambda: self.gui.use(CreditsScreen), 20)
        self.add_button((self.mid_width - 30, 410), "Quitter", self.gui.destroy, 20)
