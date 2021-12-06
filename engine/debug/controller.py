import pygame.event
from math import log


class Controller:
    def __init__(self, scene):
        self._scene = scene
    
    def tick(self, dt):
        car = self._scene.user_car
        car.wheel_speed = 0
        car.braking = False
        car.steer_angle = 0
        
        if pygame.key.get_pressed()[pygame.K_z]:
            if pygame.key.get_pressed()[pygame.K_s]:
                car.braking = True
            else:
                if car.get_actual_front_wheels_speed() < -1:
                    car.braking = True
                car.wheel_speed = 120
        elif pygame.key.get_pressed()[pygame.K_s]:
            if car.get_actual_front_wheels_speed() > 1:
                car.braking = True
            car.wheel_speed = -60
        
        if pygame.key.get_pressed()[pygame.K_q]:
            car.steer_angle += -10 / max(10, abs(car.get_actual_front_wheels_speed()))
        if pygame.key.get_pressed()[pygame.K_d]:
            car.steer_angle += 10 / max(10, abs(car.get_actual_front_wheels_speed()))
    
    def handle(self, event: pygame.event.Event):
        pass
        """if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                self._scene.user_car.wheel_speed = 0
            if event.key == pygame.K_s:
                self._scene.user_car.wheel_speed = 0
            if event.key == pygame.K_q:
                self._scene.user_car.steer_angle = 0
            if event.key == pygame.K_d:
                self._scene.user_car.steer_angle = 0"""
