from abc import ABC


class Modeled(ABC):
    def __init__(self, model):
        self._model = model
    
    @property
    def model(self):
        return self._model
    
    @property
    def hitbox(self):
        return self._model.hitbox
