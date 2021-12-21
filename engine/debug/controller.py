import pygame.event
from math import log


class Controller:
    def __init__(self, scene):
        self._scene = scene
    
    def tick(self, dt):
        user_controls = []
        if pygame.key.get_pressed()[pygame.K_z]:
            user_controls.append("z")
        if pygame.key.get_pressed()[pygame.K_s]:
            user_controls.append("s")
        if pygame.key.get_pressed()[pygame.K_q]:
            user_controls.append("q")
        if pygame.key.get_pressed()[pygame.K_d]:
            user_controls.append("d")
        
        self.handle_control(self._scene.user_car, user_controls)
        
        second_controls = []
        if pygame.key.get_pressed()[pygame.K_UP]:
            second_controls.append("z")
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            second_controls.append("s")
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            second_controls.append("q")
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            second_controls.append("d")
        
        self.handle_control(self._scene.world.cars[1], second_controls)
        
        if pygame.key.get_pressed()[pygame.K_r]:
            self._scene.reset()
    
    def handle_control(self, car, controls):
        car.wheel_speed = 0
        car.braking = False
        car.steer_angle = 0
        if "z" in controls:
            if "s" in controls:
                car.braking = True
            else:
                if car.get_actual_front_wheels_speed() < -1:
                    car.braking = True
                car.wheel_speed = 12000
        elif "s" in controls:
            if car.get_actual_front_wheels_speed() > 1:
                car.braking = True
            car.wheel_speed = -6000
        
        if "q" in controls:
            car.steer_angle += -20 / max(20, abs(car.get_actual_front_wheels_speed()))
        if "d" in controls:
            car.steer_angle += 20 / max(20, abs(car.get_actual_front_wheels_speed()))
            
