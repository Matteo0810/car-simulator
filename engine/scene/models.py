from engine.model.objloader import ObjLoader
from engine.model.polygon.polygon import Polygon


class Models:

    def __init__(self):
        self._models: dict[int, Polygon] = dict()
        self._model_id = 1

    def add(self, path: str) -> Polygon:
        model = ObjLoader.load(path)
        polygon = model.get_polygon()
        self._models[self._model_id] = polygon
        self._model_id += 1
        return polygon

    def get(self, model_id: int) -> Polygon:
        if model_id in self._models:
            return self._models[model_id]
        raise ValueError('Objet introuvable')

    def all(self):
        return self._models.values()
