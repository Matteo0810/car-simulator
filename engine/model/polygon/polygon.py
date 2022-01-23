import re

from engine.model.animations.animations import Animations
from engine.model.polygon.face import Face


class Polygon:

    def __init__(self, meshes: list, faces: dict):
        self._faces = []
        self._camera = None
        for material, faces_ in faces.items():
            for face in faces_:
                self._faces.append(self._get_face(face, material, meshes))
        self._animations = Animations(self)
        self.rotate('x', -90)

    def rotate(self, axis: str, angle: float):
        for vertex in self._meshes:
            vertex.rotate(axis, angle)
        return self

    def set_rotation(self, axis: str, angle: float):
        for vertex in self._meshes:
            vertex.set_rotation(axis, angle)
        return self

    def move(self, dx, dy, dz):
        for vertex in self._meshes:
            vertex.move(dx, dy, dz)
        return self

    def set_position(self, x, y, z):
        for vertex in self._meshes:
            vertex.set_obj_pos(x, y, z)
        return self

    def set_camera(self, camera):
        self._camera = camera
        for face in self._faces:
            face.set_camera(camera)
    
    def get_animations(self):
        return self._animations

    def _get_face(self, face_metadata: list, material, meshes) -> Face:
        props = [[int(element) - 1 for element in re.split('[/| ]+', metadata)] for metadata in face_metadata]
        return Face([meshes[prop[0]] for prop in props], material)
    
    @property
    def faces(self):
        return self._faces
    
    @property
    def _meshes(self):
        return list(set(sum((face._meshes for face in self._faces), [])))
