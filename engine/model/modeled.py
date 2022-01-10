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
        first = None
        second = None
        
        for point in self.hitbox:
            dist = point.distance(position)
            if first is None or dist < min_dist:
                min_dist = dist
                first = point
        
        for point in self.hitbox:
            if point == first:
                continue
            dist = point.distance(position)
            if second is None or dist < min_dist:
                min_dist = dist
                second = point
        
        proj = first + (position - first).dot(second - first) * (second - first) / ((second - first).length() ** 2)
        if proj.distance(first) < second.distance(first):
            if proj.distance(second) < second.distance(first):
                return proj
            else:
                return first
        else:
            return second
