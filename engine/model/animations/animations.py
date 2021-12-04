from engine.model.animations.animation import Animation


class Animations:

    def __init__(self, polygon):
        self._polygon = polygon
        self._animations = dict()

    def add(self, name: str, callback) -> Animation:
        animation = callback(Animation(name, self._polygon))
        self._animations[name] = animation
        return animation

    def get(self, name: str) -> Animation:
        if name in self._animations:
            return self._animations[name]
        raise ValueError(f'Animation \'{name}\' introuvable.')

    def all(self):
        return self._animations.values()

    def update(self, animation: Animation):
        self._animations[animation.get_name()] = animation
