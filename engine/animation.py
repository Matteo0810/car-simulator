class Animation:

    def __init__(self, name: str):
        self._name = name
        self._frames: [int, object] = dict()
        self._played = False

        self._keys = 1

    def add_frame(self, callback):
        self._frames[self._keys] = callback

    def play(self):
        self._played = True
        while self._keys <= len(self._frames) and self._played:
            self._frames[self._keys]()
            self._keys += 1

    def stop(self):
        self._played = False
        self._keys = 0

    def pause(self):
        self._played = False

    def resume(self):
        self._played = True
