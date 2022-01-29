from engine.model.objloader import ObjLoader
from engine.model.polygon.polygon import Polygon
from helpers.dotenv import get_env
from helpers.vector import Vector3


class Models(dict):

    def __init__(self, camera):
        super().__init__()
        self._model_id = 1
        self._camera = camera

    def add(self, path: str, position: Vector3 = None, size: float = 1) -> Polygon:
        path = f'{get_env("ASSETS_DIR")}models/{path}'
        model = ObjLoader.load(path, position=position, size=size)
        polygon = model.get_polygon()
        polygon.set_camera(self._camera)
        self[self._model_id] = polygon
        self._model_id += 1
        return polygon

    def get(self, model_id: int) -> Polygon:
        if model_id in self:
            return self[model_id]
        raise ValueError('Model introuvable')

    def all(self):
        return self.values()