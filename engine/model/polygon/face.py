from engine.model.material.material import Material
from helpers.vector import Vector3
from helpers.color import Color


class Face:

    def __init__(self, meshes: list, material: Material):
        self._meshes = meshes
        self._material = material

    def _flatten(self):
        flatten_list = list(map(lambda vertex: vertex.to_2d(), self._meshes))
        return [vertex for mesh in flatten_list for vertex in mesh]

    def create(self, canvas):
        canvas.create_polygon(self._flatten(), fill=self._material.get_color())

    def get_shaders(self):
        # TODO a fix scalaire des vecteurs
        v1 = Vector3(*self._meshes[1]) - Vector3(*self._meshes[0])
        v2 = Vector3(*self._meshes[2]) - Vector3(*self._meshes[1])
        normal = v1.cross(v2).fast_normalized()
        shade = max(0, normal.dot(Vector3(0, 0, -1)) * .5 + .5)
        r, g, b = tuple(self._material.get_color())
        return Color.from_list([r*shade, g*shade, b*shade, 1])
