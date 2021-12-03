from engine.model.polygon.vertex import Vertex
from engine.model.polygon.face import Face
from engine.model.polygon.texture import Texture
from engine.model.polygon.polygon import Polygon
import re


class ObjLoader:

    def __init__(self, content: list):
        self._content = [line.replace('\n', '').split() for line in content if len(line) > 1]

        self._meshes = self._get_meshes()
        self._textures = self._get_textures()
        self._faces = self._get_faces()

        self._polygon = Polygon(self._faces)

    @staticmethod
    def load(relative_path: str):
        return ObjLoader(open(relative_path, 'r', encoding="utf-8").readlines())

    def _get_meshes(self) -> list:
        return [Vertex(vertex[1:]) for vertex in self._content if vertex[0] == 'v']

    def _get_textures(self) -> list:
        return [Texture(texture[1:]) for texture in self._content if texture[0] == 'vt']

    def _get_faces(self) -> list:
        return [self._get_face(face[1:]) for face in self._content if face[0] == 'f']

    def _get_face(self, face_metadata: list) -> Face:
        props = [[int(element) - 1 for element in re.split('[/| ]+', metadata)] for metadata in face_metadata]
        return Face([self._meshes[prop[0]] for prop in props])

    def get_polygon(self):
        return self._polygon
