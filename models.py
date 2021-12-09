from engine.model.objloader import ObjLoader
from engine.model.polygon.polygon import Polygon


class Models(dict):

    def __init__(self):
        self._model_id = 1

    def add(self, path: str) -> Polygon:
        model = ObjLoader.load(path)
        polygon = model.get_polygon()
        self[self._model_id] = polygon
        self._model_id += 1
        return polygon

    def get(self, model_id: int) -> Polygon:
        if model_id in self:
            return self[model_id]
        raise ValueError('Objet introuvable')

    def all(self):
        return self.values()

    def update(self, canvas, callback=None):
        for polygon in self.all():
            if callback:
                callback(polygon)
            polygon.render(canvas)