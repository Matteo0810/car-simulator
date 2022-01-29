class EventEmitter:

    def __init__(self):
        self._callbacks = {}

    def emit(self, name):
        if name in self._callbacks:
            # print(f'[EVENT DEBUG] {name} handeled !')
            self._callbacks[name]()

    def on(self, name, callback):
        self._callbacks[name] = callback
