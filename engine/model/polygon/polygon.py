from engine.model.animation import Animation


class Polygon:

    def __init__(self, faces: list):
        self._faces = faces
        self._animations = dict()

    def add_animation(self, name: str) -> Animation:
        animation = Animation(name)
        self._animations[name] = animation
        return animation

    def get_animation(self, name: str) -> Animation:
        if name in self._animations:
            return self._animations[name]
        raise ValueError(f'Animation \'{name}\' introuvable.')

    def update_animation(self, animation: Animation):
        self._animations[animation.get_name()] = animation

    def rotate(self, axis: str, angle: float):
        for face in self._faces:
            face.rotate(axis, angle)

    def move(self, axis: str, newPos: float):
        for face in self._faces:
            face.move(axis, newPos)

    def rescale(self, scale: int):
        for face in self._faces:
            face.rescale(scale)

    def get_scale(self):
        return self._faces[0].get_scale()

    def render(self, canvas):
        for face in self._faces:
            face.create(canvas)
