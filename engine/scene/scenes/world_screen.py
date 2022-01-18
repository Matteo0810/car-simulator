from engine.scene.scene import Scene


class WorldScreen(Scene):

    def __init__(self, root):
        super().__init__(root)
        self._set_ground()
        self._default_camera.move(0, 10, 1)
        self.get_models().update(self)

    def _set_ground(self):
        self.get_models().add('ground/ground', size=10)

    @staticmethod
    def with_(world):
        return type("WorldScreen_Impl", (WorldScreen,), {"world": world})
