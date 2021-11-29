from engine.polygon.vertex import Vertex
from engine.polygon.face import Face


class Polygon:

    def __init__(self, meshes: list[Vertex], faces: list[Face]):
        self._meshes = meshes
        self._faces = faces

    def rotate(self, axis: str, angle: float):
        for vertex in self._meshes:
            vertex.rotate(axis, angle)

    def move(self, axis: str, newPos: float):
        for vertex in self._meshes:
            vertex.move(axis, newPos)

    def render(self, canvas):
        for face in self._faces:
            face.create(canvas)
