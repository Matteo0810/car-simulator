import threading
from time import sleep

from engine.ai import car_ai


class PFThread(threading.Thread):
    def __init__(self, car, scene):
        super().__init__()
        self._car = car
        self._scene = scene
        self._stopped = False
    
    def run(self):
        sleep(1)
        while threading.main_thread().is_alive() and not self._stopped:
            if isinstance(self._car.ai, car_ai.AIImpl):
                self._car.ai.pathfinding(self._scene)
            sleep(0.05)
    
    def stop(self):
        self._stopped = True
