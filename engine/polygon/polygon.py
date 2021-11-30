class Polygon:

    def __init__(self, faces: list):
        self._faces = faces

    def rotate(self, axis: str, angle: float):
        for face in self._faces:
            face.rotate(axis, angle)

    def move(self, axis: str, newPos: float):
        for face in self._faces:
            face.move(axis, newPos)

    def render(self, canvas):
        for face in self._faces:
            face.create(canvas)
