from engine.model.material.material import Material


class Face:

    def __init__(self, meshes: list, material: Material):
        self._meshes = meshes
        self._material = material

    def _flatten(self):
        flatten_list = list(map(lambda vertex: vertex.to_2d(), self._meshes))
        return [vertex for mesh in flatten_list for vertex in mesh]

    def create(self, canvas):
        canvas.create_polygon(self._flatten(), fill=self._material.get_color())
