from helpers.dotenv import get_env


class Controller:

    def __init__(self, scene):
        self._scene = scene
        self._models = self._scene.get_models()

        self._size = (get_env('WIDTH'), get_env('HEIGHT'))

        self._previous = []
        self._previous_z = None
        self._scale = 0

    def setup(self):
        self._scene.bind('<MouseWheel>', self._zoom)

        self._scene.bind('<B1-Motion>', self._rotate)
        self._scene.bind('<ButtonRelease-1>', self._reset_rotate)

        self._scene.bind('<B3-Motion>', self._rotate_z)
        self._scene.bind('<ButtonRelease-3>', self._reset_rotate)

        self.init_labels()
        return self

    def init_labels(self):
        width, height = self._size

        self._scene.add_label((width - 170, height - 170), "r : reload")
        self._scene.add_label((width - 170, height - 130), "roulette : taille")
        self._scene.add_label((width - 185, height - 90), "z-q-s-d : mouvement")
        self._scene.add_label((width - 170, height - 50), "souris : rotation")
        
    def handle_keys(self, event):
        self.get_moves(event)
        return self

    def get_moves(self, event):
        moves = {
            'z': ('y', -0.5),
            'q': ('x', -0.5),
            'd': ('x', 0.5),
            's': ('y', 0.5)
        }
        self._scene.update(lambda model: self._move_model(moves, model, event.char))

    def _move_model(self, moves, model, char):
        r = moves.get(char)
        if r is not None:
            model.move(r[0], r[1])

    def _zoom(self, event):
        self._scale += (-1, 1)[event.delta > 0]

        if event.delta > 0 and self._scale < 0:
            self._scale = 1
        elif event.delta < 0 and self._scale > 0:
            self._scale = 1

        self._scene.get_camera().set_zoom(self._scene.get_camera().zoom + (-0.05, 0.05)[event.delta > 0])
        self._scene.update()

    def _reset_rotate(self, _):
        self._previous = []
        self._previous_z = None

    def _rotate(self, event):
        if self._previous:
            camera = self._scene.get_camera()
            camera.set_direction(camera.yaw + (event.x - self._previous[0]) / 20, camera.pitch + (event.y - self._previous[1]) / 20)
            self._scene.update()
        self._previous = [event.x, event.y]

    def _rotate_z(self, event):
        # la 3eme rotation n'est plus possible (rotation y: le roll, pas implémenté, la caméra est définie par yaw et pitch)
        
        #if self._previous_z:
        #    self._scene.update(lambda model: model.rotate('z', (event.x - self._previous_z) / 20))
        #self._previous_z = event.x
        pass

    def _rotate_xy(self, model, event):
        model.rotate('x', (event.y - self._previous[1]) / 20)
        model.rotate('y', (event.x - self._previous[0]) / 20)
