from engine.model.modeled import Modeled
from engine.model.model import Model
from helpers.vector import Vector2


class Obstacle(Modeled):
    def __init__(self, model: Model, position: Vector2):
        super().__init__(model)
        self._position = position
    
    @property
    def position(self):
        return self._position
