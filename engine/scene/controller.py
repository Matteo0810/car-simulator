class Controller:

    def __init__(self, scene):
        self._scene = scene
        self._previous = []

    def handle(self):
        self._scene.bind('<B1-Motion>', self._rotate)
        self._scene.bind('<ButtonRelease-1>', self._reset_rotate)
        self._scene.bind('<MouseWheel>', self._zoom)

    def _zoom(self, event):
        if event.delta > 0:
            # zoom in
            pass
        elif event.delta < 0:
            # zoom out
            pass

    def _reset_rotate(self, _):
        self._previous = []

    def _rotate(self, event):
        if self._previous:
            self._scene.get_model(1).rotate('x', (event.y - self._previous[1]) / 20)
            self._scene.get_model(1).rotate('y', (event.x - self._previous[0]) / 20)
            self._scene.update()
        self._previous = [event.x, event.y]
