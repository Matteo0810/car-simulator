from engine.model.material.material import Material
from engine.model.polygon.tk_polygon import TkPolygon
from helpers.vector import Vector3
from helpers.color import Color


class Face:

    def __init__(self, meshes: list, material: Material):
        self._meshes = meshes
        self._material = material
        self._camera = None

    def _flatten(self):
        flatten_list = list(map(lambda vertex: vertex.to_2d(self._camera), self._meshes))
        return [vertex for mesh in flatten_list for vertex in mesh]

    def create(self, canvas):
        points = self._flatten()
        if not any(self._camera.is_in_plan(p) for p in points):
            canvas.create_polygon(points, fill=self.get_shaders())
            return TkPolygon(points, self.get_shaders())
        return TkPolygon([], Color(0, 0, 0))
    
    def get_shaders(self):
        direction = self._camera.direction  # of camera
        
        light_direction = Vector3(0.1, 0.5, -1).normalized()
        
        v1 = self._meshes[0].position - self._meshes[-1].position
        v2 = self._meshes[-1].position - self._meshes[-2].position
        normal = v1.cross(v2).fast_normalized()
        if direction.dot(normal) < 0:
            normal = -normal
        shade = max(0, normal.dot(light_direction) * .6 + .4)
        r, g, b = tuple(self._material.get_color())
        return Color.from_list([r * shade, g * shade, b * shade, 1])

    def avg_dist(self):
        return -sum([vertex.plan_distance(self._camera) for vertex in self._meshes]) / len(self._meshes)
    
    def set_camera(self, camera):
        self._camera = camera
