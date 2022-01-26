import random

from engine.scene.scene import Scene
from engine.scene.scenes.credits_screen import CreditsScreen
from engine.scene.scenes.settings_screen import SettingsScreen
from engine.scene.scenes.worlds_screen import WorldsScreen
from helpers.vector import Vector3, Vector2
from helpers.utils import lerp


class TitleScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.add_label((self.mid_width - 130, 200), "Car simulator", 25)

        models = self.get_models()
        
        self.get_camera().set_direction(0, 0)
        self.get_camera().set_position(0, 0, -1)
        self.get_camera().set_zoom(1)

        car = models.add('car/car', position=Vector3(3, 10, -2.5))
        car.rotate('y', 0).rotate('z', -30)

        offset = Vector3(3.46, 6, 0)*1.1
        road = models.add('roads/thin_road', position=Vector3(2.8, 10, -3) - 0.5 * offset)
        road.rotate('y', 0).rotate('z', -30)
        for i in range(9):
            road = models.add('roads/thin_road', position=Vector3(2.8, 10, -3) + i * offset)
            road.rotate('y', 0).rotate('z', -30)
        
        tree_positions = [
            Vector2(-3, 10),
            Vector2(-2, 18),
            Vector2(4, 23),
            Vector2(-1, 29),
            Vector2(-12, 33),
            Vector2(2, 37),
            Vector2(-6, 29),
        ]
        for i in range(len(tree_positions)):
            x, y = tree_positions[i]
            
            tree_model = random.randint(0, 0)
            if tree_model == 0:
                tree = models.add("tree1/lowpolytree", position=Vector3(x, y, -1))
                tree.rotate('x', 180).rotate('z', random.randint(0, 360))
            if tree_model == 1:
                tree = models.add("tree2/tree", size=0.2, position=Vector3(x, y, -2.7))
                tree.rotate('x', 180).rotate('z', random.randint(0, 360))
        
        ground = models.add('grounds/ground_forest/ground', size=99, position=Vector3(0, 100, -3.1))
        #build_ground(models, self.get_camera(), 5, -50, 5, 50, 50, amp=5)
        
        self.add_button((self.mid_width - 30, 260), "Mondes", lambda: self.gui.use(WorldsScreen), 20)
        self.add_button((self.mid_width - 30, 260 + 49), "Options", lambda: self.gui.use(SettingsScreen), 20)
        self.add_button((self.mid_width - 30, 260 + 49 * 2), "Crédits", lambda: self.gui.use(CreditsScreen), 20)
        self.add_button((self.mid_width - 30, 260 + 49 * 3), "Quitter", self.gui.destroy, 20)
    
    def clear(self):
        super().clear()
        for i in range(self.height):
            nr = int(lerp(150, 150, i / self.height))
            ng = int(lerp(100, 200, i / self.height))
            nb = int(lerp(0, 255, i / self.height))
            color = "#%02x%02x%02x" % (nr, ng, nb)
            self.create_line(0, i, self.width, i, tags=("gradient",), fill=color)
