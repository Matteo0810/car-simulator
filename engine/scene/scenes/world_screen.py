from engine.scene.scene import Scene
from abc import ABC
from world.world import World


class WorldScreen(Scene, ABC):
    world = None
    def __init__(self, root):
        super().__init__(root)

def get_world_screen_type(world: World):
    return type("_WorldScreen", (WorldScreen,), {"world": world})
