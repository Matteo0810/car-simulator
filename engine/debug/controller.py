from math import copysign

import pygame.event

from engine.car_ai import AI

BASE_CONTROLS = {
    "z": pygame.K_z,
    "q": pygame.K_q,
    "s": pygame.K_s,
    "d": pygame.K_d
}


class PygameController(AI):
    def __init__(self, car, scene, fw_speed, bw_speed, controls=BASE_CONTROLS):
        self._scene = scene
        self._fw_speed = fw_speed
        self._bw_speed = bw_speed
        self._controls = controls
        self._car = car
    
    def get_wheel_speed(self):
        if pygame.key.get_pressed()[self._controls["z"]]:
            if not pygame.key.get_pressed()[self._controls["s"]]:
                return self._fw_speed
            else:
                return 0
        elif pygame.key.get_pressed()[self._controls["s"]]:
            return -self._bw_speed
        actual_speed = self._car.get_actual_back_wheels_speed()
        return 0 if abs(actual_speed) < self._car.model.acceleration else actual_speed - copysign(self._car.model.acceleration, actual_speed)

    def get_steer_angle(self):
        steer_angle = 0
        if pygame.key.get_pressed()[self._controls["q"]]:
            steer_angle += -5 / max(5, abs(self._car.get_actual_front_wheels_speed()))
        if pygame.key.get_pressed()[self._controls["d"]]:
            steer_angle += 5 / max(5, abs(self._car.get_actual_front_wheels_speed()))
        return steer_angle

    def is_braking(self):
        if pygame.key.get_pressed()[self._controls["z"]]:
            if pygame.key.get_pressed()[self._controls["s"]]:
                return True
        return False
