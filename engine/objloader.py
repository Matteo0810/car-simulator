from .helpers.vertex import Vertex
from .helpers.face import Face


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
            open(relative_path, 'r').readlines(),
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
                vertex_textures.append((vertex_texture[0], vertex_texture[1]))
        return vertex_textures

    def _get_faces(self):
        faces = []
        meshes = self._vertex_meshes

        for face in self._content:
            if face[0] == "f":
                face.pop(0)
                props = [[int(i)-1 for i in j.split('/')] for j in face]
                faces.append(Face(
                    meshes[props[0][0]], meshes[props[1][0]], meshes[props[2][0]]))
        return faces

    def rotate(self, axis, angle):
        for vertex in self._vertex_meshes:
            vertex.rotate(axis, angle)

    def move(self, axis, newPos):
        for vertex in self._vertex_meshes:
            vertex.rotate(axis, newPos)

    def render(self, canvas):
        for face in self._faces:
            face.create(canvas)
