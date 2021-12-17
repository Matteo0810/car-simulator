from engine.model.polygon.vertex import Vertex
from engine.model.polygon.polygon import Polygon
from engine.model.material.mtl_loader import MTLLoader


class ObjLoader:

    def __init__(self, content: list, mtl_loader: MTLLoader, position: tuple = None, size: int = None):
        self._content = [line.split() for line in content if len(line) > 1]

        # polygon
        self._position = position
        self._size = size
        self._meshes = self._get_meshes()
        self._faces = self._get_faces()

        # materials
        self._materials = mtl_loader.get_materials()
        self._material = self._get_material()

        self._polygon = Polygon(self._meshes, self._faces, self._material)

    @staticmethod
    def load(relative_path: str, position: tuple = None, size: tuple = None):
        if len(relative_path.split('.')) < 2:
            relative_path += '.obj'
        return ObjLoader(
            open(relative_path, 'r', encoding="utf-8").readlines(),
            MTLLoader.load(relative_path),
            position,
            size
        )

    def _get_material(self):
        for content in self._content:
            if content[0] == 'usemtl':
                return self._materials[content[1]]
        return None

    def _get_meshes(self) -> list:
        return [Vertex(vertex[1:], self._position, self._size) for vertex in self._content if vertex[0] == 'v']

    def _get_faces(self) -> list:
        return [face[1:] for face in self._content if face[0] == 'f']

    def get_polygon(self):
        return self._polygon
