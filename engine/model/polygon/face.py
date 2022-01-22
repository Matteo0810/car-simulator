from engine.model.material.material import Material
from engine.scene.camera import Camera
from helpers.vector import Vector3
from helpers.color import Color


class Face:

    def __init__(self, meshes: list, material: Material, camera: Camera):
        self._meshes = meshes
        self._material = material
        self._camera = camera

    def _flatten(self):
        flatten_list = list(map(lambda vertex: vertex.to_2d(self._camera), self._meshes))
        return [vertex for mesh in flatten_list for vertex in mesh]

    def create(self, canvas):
        canvas.create_polygon(self._flatten(), fill=self.get_shaders())

    def get_shaders(self):
        direction = self._camera.direction  # of camera
        
        light_direction = Vector3(0.1, 0.5, -1).normalized()
        
        v1 = Vector3(*self._meshes[0]) - Vector3(*self._meshes[-1])
        v2 = Vector3(*self._meshes[-1]) - Vector3(*self._meshes[-2])
        normal = v1.cross(v2).fast_normalized()
        if direction.dot(normal) < 0:
            normal = -normal
        shade = max(0, normal.dot(light_direction) * .6 + .4)
        r, g, b = tuple(self._material.get_color())
        return Color.from_list([r * shade, g * shade, b * shade, 1])

    def avg_dist(self):
        return -sum([vertex.plan_distance(self._camera) for vertex in self._meshes]) / len(self._meshes)
