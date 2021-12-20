from engine.model.animations.animations import Animations
from engine.model.polygon.face import Face
import re


class Polygon:

    def __init__(self, meshes: list, faces: dict):
        self._meshes = meshes
        self._faces = faces
        self._camera = None
        self._animations = Animations(self)

    def rescale(self, scale: int):
        for vertex in self._meshes:
            vertex.rescale(scale)

    def rotate(self, axis: str, angle: float):
        for vertex in self._meshes:
            vertex.rotate(axis, angle)

    def move(self, axis: str, newPos: float):
        for vertex in self._meshes:
            vertex.move(axis, newPos)

    def render(self, canvas):
        for face in self._sort_z():
            face.create(canvas)

    def set_camera(self, camera):
        self._camera = camera

    def get_scale(self):
        return self._meshes[0].get_scale()

    def get_animations(self):
        return self._animations

    def _get_face(self, face_metadata: list, material) -> Face:
        props = [[int(element) - 1 for element in re.split('[/| ]+', metadata)] for metadata in face_metadata]
        return Face([self._meshes[prop[0]] for prop in props], material, self._camera)

    def _sort_z(self) -> list:
        result = []
        for material, faces in self._faces.items():
            for face in faces:
                result.append(self._get_face(face, material))
        return sorted(
            result,
            key=lambda vertex: vertex.avg_z()
        )
