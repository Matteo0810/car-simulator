from engine.model.polygon.vertex import Vertex
from engine.model.polygon.polygon import Polygon
from engine.model.material.mtl_loader import MTLLoader
from helpers.vector import Vector3


class ObjLoader:

    def __init__(self, content: list, mtl_loader: MTLLoader, distance=6, position=None, size=1):
        self._materials = mtl_loader.get_materials()
        self._content = [line.split() for line in content if len(line) > 1]

        # positions
        self._position = position or Vector3(0, 0, 0)
        self._size = size
        self._distance = distance

        # polygon
        self._meshes = self._get_meshes()
        self._faces = self._get_faces()

        self._polygon = Polygon(self._meshes, self._faces)

    @staticmethod
    def load(relative_path: str, position: Vector3 = None, size: int = 1, distance: int = 6, material_path: str = None):
        if len(relative_path.split('.')) < 2:
            relative_path += ".obj"
        return ObjLoader(
            open(relative_path, 'r', encoding="utf-8").readlines(),
            MTLLoader.load(material_path or relative_path),
            distance, position, size
        )

    def _get_meshes(self) -> list:
        return [Vertex(Vector3(*element[1:]) * self._size, self._position, self._distance) for element in self._content if element[0] == 'v']

    def _get_faces(self) -> dict:
        result, content = {}, self._content
        i, j = 0, 0
        while i < len(content):
            if content[i][0] == 'usemtl':
                material = self._materials[content[i][1]]
                if material not in result:
                    result[material] = []
                j = i + 1
                while j < len(content) and content[j][0] != 'usemtl':
                    if content[j][0] == 'f':
                        result[material].append(content[j][1:])
                    j += 1
            i += 1
        return result

    def get_polygon(self):
        return self._polygon
