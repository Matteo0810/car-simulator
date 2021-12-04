class Animation:

    def __init__(self, name: str, polygon):
        self._name = name
        self._polygon = polygon
        self._frames = list()
        self._played = False

        self._keys = 0

    def play(self):
        self._played = True
        while self._keys < len(self._frames) and self._played:
            self._frames[self._keys](self._polygon)
            self._keys += 1

    def stop(self):
        self._played = False
        self._keys = 0

    def pause(self):
        self._played = False

    def resume(self):
        self._played = True

    def get_name(self):
        return self._name
