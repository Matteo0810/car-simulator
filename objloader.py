from engine.model.polygon.vertex import Vertex
from engine.model.polygon.polygon import Polygon
from engine.model.material.mtl_loader import MTLLoader


class ObjLoader:

    def __init__(self, content: list, mtl_loader: MTLLoader):
        # materials
        self._materials = mtl_loader.get_materials()

        self._content = [line.split() for line in content if len(line) > 1]
        self._content = self._parse()

        # polygon
        self._meshes = self._get_meshes()
        self._faces = self._get_faces()
        
        self._polygon = Polygon(self._meshes, self._faces)

    @staticmethod
    def load(relative_path: str):
        return ObjLoader(
            open(relative_path, 'r', encoding="utf-8").readlines(),
            MTLLoader.load(relative_path)
        )

    def _parse(self):
        result, content = {}, self._content
        i, j = 0, 0
        while i < len(content):
            if content[i][0] == 'usemtl' and content[i][1] not in result:
                result[content[i][1]] = []
                j = i + 1
                while j < len(content) and content[j][0] != 'usemtl':
                    result[content[i][1]].append(content[j])
                    j += 1
            i += 1
        return result

    def _get_meshes(self) -> list:
        result =  []
        for _, v in self._content.items():
            for e in v:
                if e[0] == 'v':
                    result.append(Vertex(e[1:]))
        return result

    def _get_faces(self) -> list:
        result = []
        for k, v in self._content.items():
            for e in v:
                if e[0] == 'f':
                    result.append(e[1:] + [self._materials[k]])
        return result

    def get_polygon(self):
        return self._polygon
