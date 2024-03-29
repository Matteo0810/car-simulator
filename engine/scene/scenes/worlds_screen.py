from engine.scene.scene import Scene
from engine.scene.scenes.world_screen import WorldScreen
from world.world import World
from helpers.utils import get_folder_content


class WorldsScreen(Scene):

    def __init__(self, root):
        super().__init__(root, title="Mondes")
        self.worlds = [World.load(open(file_name, mode='r', encoding='utf-8').read())
                       for file_name in get_folder_content('assets/worlds')]

        for world, i in zip(self.worlds, range(len(self.worlds))):
            self.add_button((self.mid_width - 30, 260 + 50 * i), world.props['name'],
                            lambda: self.gui.use(WorldScreen.with_(world)), 20)

        self.add_button((self.mid_width - 30, 260 + 50 * len(self.worlds)), "Retour", self.gui.use_last_scene, 20)
