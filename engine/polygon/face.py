class Face:

    def __init__(self, meshes):
        self._meshes = meshes
        self._flatten_meshes = list(map(lambda vertex: vertex.to_2d(), meshes))

    def rotate(self, axis: str, angle: float):
        for vertex in self._meshes:
            vertex.rotate(axis, angle)

    def move(self, axis: str, angle: float):
        for vertex in self._meshes:
            vertex.move(axis, angle)

    def _get_flatten_meshes(self):
        return [vertex for mesh in self._flatten_meshes for vertex in mesh]

    def create(self, canvas):
        canvas.create_polygon(
            self._get_flatten_meshes(),
            outline="gray"
        )