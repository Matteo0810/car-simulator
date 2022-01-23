from engine.model.objloader import ObjLoader
from engine.model.polygon.polygon import Polygon
from helpers.dotenv import get_env
from helpers.vector import Vector3


class Models(dict):

    def __init__(self, camera, loader):
        super().__init__()
        self._model_id = 1
        self._camera = camera
        self._loader = loader

    def add(self, path: str, position: Vector3 = None, size: int = 1, distance: int = 6, material_path: str = None) -> Polygon:
        path = f'{get_env("ASSETS_DIR")}models/{path}'
        model = ObjLoader.load(path, position=position, size=size, distance=distance, material_path=material_path)
        polygon = model.get_polygon()
        polygon.set_camera(self._camera)
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
        if len(self) < 1:
            return
        faces = []
        for polygon in self.all():
            if callback:
                callback(polygon)
            faces.extend(polygon.faces)
        
        for face in sorted(faces, key=lambda f: f.avg_dist()):
            face.create(canvas)
