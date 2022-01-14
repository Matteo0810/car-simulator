from abc import ABC

from engine.scene.scene import Scene
from world.world import World


class WorldScreen(Scene, ABC):
    world = None
    
    def __init__(self, root):
        super().__init__(root)

