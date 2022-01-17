from engine.scene.scene import Scene


class WorldScreen(Scene):

    def __init__(self, root):
        super().__init__(root)
        self._set_ground()

    def _set_ground(self):
        self.get_models().add('ground/ground', size=10)

    @staticmethod
    def with_(world):
        return type("WorldScreen_Impl", (WorldScreen,), {"world": world})
