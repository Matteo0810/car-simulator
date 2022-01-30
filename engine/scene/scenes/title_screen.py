import random

from engine.scene.scene import Scene
from helpers.vector import Vector3, Vector2
from helpers.utils import lerp


class TitleScreen(Scene):

    def __init__(self, root):
        super().__init__(root, title="Car simulator")

        self.set_buttons([
            {"text": "Mondes", "callback": lambda: self.gui.use(self.gui.screens['worlds'])},
            {"text": "Crédits", "callback": lambda: self.gui.use(self.gui.screens['credits'])},
            {"text": "Quitter", "callback": self.gui.destroy}
        ])

        self.get_camera().set_direction(0, 0).set_position(0, 0, -1).set_zoom(1)

        self.get_models().add('low_car_default/car', position=Vector3(3, 10, -2.5)).rotate('y', 0).rotate('z', -30)
        self.get_models().add('grounds/ground', size=99, position=Vector3(0, 100, -3.1))

        self._render_road()
        self._render_trees()

    def _render_road(self):
        offset = Vector3(3.46, 6, 0) * 1.1
        self.get_models().add('roads/thin_road', position=Vector3(2.8, 10, -3) - 0.5 * offset) \
            .rotate('y', 0).rotate('z', -30)
        for i in range(9):
            self.get_models().add('roads/thin_road', position=Vector3(2.8, 10, -3) + i * offset) \
                .rotate('y', 0).rotate('z', -30)

    def _render_trees(self):
        tree_positions = [Vector2(-3, 10), Vector2(-2, 18), Vector2(4, 23), Vector2(-1, 29), Vector2(-12, 33),
                          Vector2(2, 37), Vector2(-6, 29)]

        for i in range(len(tree_positions)):
            x, y = tree_positions[i]
            tree_model = random.randint(0, 0)
            self.get_models().add(f'trees/tree{tree_model + 1}/tree', size=(1, 0.2)[tree_model == 1],
                                  position=Vector3(x, y, (-1, -2.7)[tree_model == 1])) \
                .rotate('x', 180).rotate('z', random.randint(0, 360))

    def clear(self):
        super().clear()
        for i in range(self.height):
            nr = int(lerp(150, 150, i / self.height))
            ng = int(lerp(100, 200, i / self.height))
            nb = int(lerp(0, 255, i / self.height))
            color = "#%02x%02x%02x" % (nr, ng, nb)
            self.create_line(0, i, self.width+2, i, tags=("gradient",), fill=color)
