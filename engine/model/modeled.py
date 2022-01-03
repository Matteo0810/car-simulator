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
    
    def nearest_hitbox_point(self, position):
        min_dist = 0
        nearest_point = None
        
        for point in self.hitbox:
            dist = point.distance(position)
            if nearest_point is None or dist < min_dist:
                min_dist = dist
                nearest_point = point
        
        return nearest_point
