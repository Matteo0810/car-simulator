class Face:

    def __init__(self, meshes):
        self._meshes = meshes

    def _flatten(self):
        flatten_list = list(map(lambda vertex: vertex.to_2d(), self._meshes))
        return [vertex for mesh in flatten_list for vertex in mesh]

    def create(self, canvas):
        canvas.create_polygon(self._flatten(), fill="gray")