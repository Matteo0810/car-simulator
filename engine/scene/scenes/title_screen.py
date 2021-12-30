from engine.scene.scene import Scene
from engine.scene.scenes.settings_screen import SettingsScreen
from engine.scene.scenes.worlds_screen import WorldsScreen


class TitleScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.add_label((self.middle_width - 130, 200), "Car simulator", 25)

        self.add_button((self.middle_width - 30, 260), "Mondes", lambda: self.gui.use(WorldsScreen), 20)
        self.add_button((self.middle_width - 30, 310), "Options", lambda: self.gui.use(SettingsScreen), 20)
        self.add_button((self.middle_width - 30, 360), "Quitter", self.gui.destroy, 20)
