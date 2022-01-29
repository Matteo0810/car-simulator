from time import time

from helpers.dotenv import get_env


class FPS:

    def __init__(self, scene):
        self._scene = scene
        self._count = 0
        self._last = time()
        self._label = None

    def _update_count(self):
        current = time()
        if (current - self._last) > 1:
            self._count = 0
            self._last = current
            return
        self._count += 1

    def update(self):
        self._update_count()
        if self._label is not None:
            self._label['text'] = f'[Dev] FPS: {self._count}'
            return
        self._label = self._scene.add_label((get_env('WIDTH') // 2, 15), f'[Dev] FPS: 0')
