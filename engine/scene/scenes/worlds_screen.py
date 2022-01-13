from engine.scene.scene import Scene
from engine.scene.scenes.world_screen import WorldScreen, get_world_screen_type
from world.world import World
import json


class WorldsScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.add_label((self.mid_width - 50, 200), "Mondes", 25)

        worlds = [World.load(json.loads(open("world/assets/world.json", mode='r').read()))]
        for world, i in zip(worlds, range(len(worlds))):
            self.add_button((self.mid_width - 30, 260 + 50 * i), "World test", lambda: self.gui.use(get_world_screen_type(world)), 20)

        self.add_button((self.mid_width - 30, 360 + 50 * len(worlds)), "Retour", self.gui.previous_scene, 20)
