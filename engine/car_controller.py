from math import copysign

from engine.ai.car_ai import AI


class CarController(AI):

    def __init__(self, scene, car=None, fw_speed=None, bw_speed=None):
        self._scene = scene
        self._car = car
        self._fw_speed = fw_speed
        self._bw_speed = bw_speed
        self._pressed_controls = []

    def handle_keys(self, event):
        self._event = event
        self.get_steer_angle()
        self.get_wheel_speed()
        self.is_braking()
        return self

    def get_wheel_speed(self):
        event = self._event
        if not event: return
        if event.char == 'z':
            return (0, self._fw_speed)[not event.char == 's']
        elif event.char == 's':
            return -self._bw_speed
        actual_speed = self._car.get_actual_back_wheels_speed()
        return 0 if abs(actual_speed) < self._car.car_type.acceleration else actual_speed - copysign(
            self._car.car_type.acceleration, actual_speed)

    def get_steer_angle(self):
        event = self._event
        if not event: return
        steer_angle = 0
        if event.char == 'q':
            steer_angle += -10 / max(10, abs(self._car.get_actual_front_wheels_speed()))
        if event.char == 'd':
            steer_angle += 10 / max(10, abs(self._car.get_actual_front_wheels_speed()))
        return steer_angle

    def is_braking(self):
        event = self._event
        if not event: return
        return event.char == 'z' and event.char == 's'
