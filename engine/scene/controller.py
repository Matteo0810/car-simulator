class Controller:

    def __init__(self, scene):
        self._scene = scene
        self._models = self._scene.get_models()
        self._previous = []

    def handle(self):
        self._scene.bind('<B1-Motion>', self._rotate)
        self._scene.bind('<ButtonRelease-1>', self._reset_rotate)
        self._scene.bind('<MouseWheel>', self._zoom)

    def _zoom(self, event):
        if event.delta > 0:
            pass
        elif event.delta < 0:
            pass

    def _reset_rotate(self, _):
        self._previous = []

    def _rotate(self, event):
        if self._previous:
            for model in self._models.all():
                model.rotate('x', (event.y - self._previous[1]) / 20)
                model.rotate('y', (event.x - self._previous[0]) / 20)
            self._scene.update()
        self._previous = [event.x, event.y]
