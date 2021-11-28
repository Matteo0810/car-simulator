from .helpers.vertex import Vertex
from .helpers.face import Face
import re


class ObjLoader:

    def __init__(self, content: list, size: tuple, distance: int, scale: int):
        self._content = [line.replace('\n', '').split() for line in content if len(line) > 1]
        self._size = size
        self._distance = distance
        self._scale = scale

        self._vertex_meshes = self._get_vertex_meshes()
        self._vertex_textures = self._get_vertex_textures()
        self._faces = self._get_faces()

    @staticmethod
    def load(relative_path: str, size: tuple, distance: int, scale: int):
        return ObjLoader(
            open(relative_path, 'r', encoding="utf-8").readlines(),
            size,
            distance,
            scale
        )

    def _get_vertex_meshes(self):
        vertex_meshes = []
        for vertex in self._content:
            if vertex[0] == "v":
                vertex.pop(0)
                vertex_meshes.append(
                    Vertex(
                        vertex[0],
                        vertex[1],
                        vertex[2], 0,
                        (self._size, self._distance, self._scale)
                    )
                )
        return vertex_meshes

    def _get_vertex_textures(self):
        vertex_textures = []
        for vertex_texture in self._content:
            if vertex_texture[0] == "vt":
                vertex_texture.pop(0)
                vertex_textures.append((float(vertex_texture[0]), float(vertex_texture[1])))
        return vertex_textures

    def _get_faces(self):
        faces = []
        meshes = self._vertex_meshes
        textures = self._vertex_textures

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
