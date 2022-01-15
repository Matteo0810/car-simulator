from engine.scene.scene import Scene


class WorldScreen(Scene):
    
    def __init__(self, root):
        super().__init__(root)
    
    @staticmethod
    def with_(world):
        return type("WorldScreen_Impl", (WorldScreen,), {"world": world})
