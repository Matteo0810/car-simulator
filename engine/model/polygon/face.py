class Face:

    def __init__(self, meshes):
        self._meshes = meshes

    def rotate(self, axis: str, angle: float):
        for vertex in self._meshes:
            vertex.rotate(axis, angle)

    def move(self, axis: str, angle: float):
        for vertex in self._meshes:
            vertex.move(axis, angle)

    def _flatten(self):
        flatten_list = list(map(lambda vertex: vertex.to_2d(), self._meshes))
        return [vertex for mesh in flatten_list for vertex in mesh]

    def create(self, canvas):
        canvas.create_polygon(
            self._flatten(),
            outline="gray"
        )