from helpers.dotenv import get_env


class Controller:

    def __init__(self, scene):
        self._scene = scene
        self._models = self._scene.get_models()

        self._size = (get_env('WIDTH'), get_env('HEIGHT'))
        self._previous = []
        self._scale = 0

    def setup(self):
        self._scene.focus_set()
        self._scene.bind('<Key>', self._move)
        self._scene.bind('<B1-Motion>', self._rotate)
        self._scene.bind('<ButtonRelease-1>', self._reset_rotate)
        self._scene.bind('<MouseWheel>', self._zoom)

        self.init_labels()

    def init_labels(self):
        width, height = self._size

        self._scene.add_label((width - 140, height - 130), "roulette : taille")
        self._scene.add_label((width - 185, height - 90), "z-q-s-d : mouvement")
        self._scene.add_label((width-150, height-50), "souris : rotation")

    def _move(self, event):
        moves = {
            'z': ('y', 0.5),
            'q': ('x', 0.5),
            'd': ('x', -0.5),
            's': ('y', -0.5)
        }

        for model in self._models.all():
            r = moves.get(event.char)
            if r is not None:
                model.move(r[0], r[1])
        self._scene.update()

    def _zoom(self, event):
        self._scale += (-1, 1)[event.delta > 0]

        if event.delta > 0 and self._scale < 0:
            self._scale = 1
        elif event.delta < 0 and self._scale > 0:
            self._scale = 1

        for model in self._models.all():
            model.rescale(model.get_scale() + self._scale)
        self._scene.update()

    def _reset_rotate(self, _):
        self._previous = []

    def _rotate(self, event):
        if self._previous:
            for model in self._models.all():
                model.rotate('x', (event.y - self._previous[1]) / 20)
                model.rotate('y', (event.x - self._previous[0]) / 20)
            self._scene.update()
        self._previous = [event.x, event.y]
