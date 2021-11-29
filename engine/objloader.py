from engine.polygon.vertex import Vertex
from engine.polygon.face import Face
from engine.polygon.texture import Texture
import re


class ObjLoader:

    def __init__(self, content: list):
        self._content = [line.replace('\n', '').split() for line in content if len(line) > 1]

        self._vertex_meshes = self._get_vertex_meshes()
        self._vertex_textures = self._get_vertex_textures()
        self._faces = self._get_faces()

    @staticmethod
    def load(relative_path: str):
        return ObjLoader(open(relative_path, 'r', encoding="utf-8").readlines())

    def _get_vertex_meshes(self):
        return [Vertex(vertex[1:]) for vertex in self._content if vertex[0] == 'v']

    def _get_vertex_textures(self):
        return [Texture(texture[1:]) for texture in self._content if texture[0] == 'vt']

    def _get_faces(self):
        faces = []
        meshes = self._vertex_meshes

        for face in self._content:
            if face[0] == "f":
                face.pop(0)
                props = [[int(i)-1 for i in re.split('/+', j)] for j in face]
                vA, vB, vC = meshes[props[0][0]], meshes[props[1][0]], meshes[props[2][0]]
                faces.append(Face(vA, vB, vC))
        return faces

    def rotate(self, axis: str, angle: float):
        for vertex in self._vertex_meshes:
            vertex.rotate(axis, angle)

    def move(self, axis: str, newPos: float):
        for vertex in self._vertex_meshes:
            vertex.move(axis, newPos)

    def render(self, canvas):
        for face in self._faces:
            face.create(canvas)
