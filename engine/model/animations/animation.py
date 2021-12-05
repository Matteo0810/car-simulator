import time, threading


class Animation:

    def __init__(self, name: str, polygon):
        self._name = name
        self._polygon = polygon
        self._frames = list()
        self._played = False

        self._keys = 0

    def play(self, scene):
        threading.Thread(target=self._play_frames, args=(scene,)).start()

    def _play_frames(self, scene):
        self._played = True
        while self._keys < len(self._frames) and self._played:
            try:
                self._frames[self._keys](self._polygon)
                scene.update()
                time.sleep(0.05)
                self._keys += 1
            except ValueError:
                raise ValueError('Function not found.')

    def add_frame(self, callback):
        self._frames.append(callback)

    def stop(self):
        self._played = False
        self._keys = 0

    def pause(self):
        self._played = False

    def resume(self):
        self._played = True

    def get_name(self):
        return self._name
