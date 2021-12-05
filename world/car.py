from math import *

from engine.physics import reconstruct_car
from helpers.dotenv import get_env
from helpers.utils import *

import pygame.draw
from pygame import Vector2


class Car:
    def __init__(self, scene, position, angle, model):
        self._wheels = [Wheel(Vector2(0, 0), 0) for _ in range(4)]
        self._model = model
        self._width = width = model.hitbox[0]
        self._length = length = model.hitbox[1]
        self._braking = False
        self._wheel_speed = 0
        self._steer_angle = 0
        self._color = model.default_color
        self._scene = scene
        
        self._acceleration = 20  # pi/s²
        
        reconstruct_car(self._wheels, width, length, hard_position=position, hard_angle=angle)
    
    def _accelerate(self, dt):
        self._color = (0, 255, 0)
        for wheel in self._wheels:
            wheel.last_position = wheel.position
        
            actual_wheel_speed = wheel.velocity.length()

            cos_angle = cos(unit_vector(wheel.angle).angle_to(wheel.velocity) / 180 * pi)
            projection = cos_angle * unit_vector(wheel.angle, actual_wheel_speed)
            
            #pygame.draw.rect(self._scene.screen, (0, 0, 0), pygame.rect.Rect(unit_vector(wheel.angle, 5) + wheel.position + Vector2(750, 500), (3, 3)))
            pygame.draw.rect(self._scene.screen, (0, 0, 255), pygame.rect.Rect(projection + wheel.position + Vector2(750, 500), (3, 3)))
            pygame.draw.rect(self._scene.screen, (255, 0, 0), pygame.rect.Rect(wheel.velocity + wheel.position + Vector2(750, 500), (3, 3)))
        
            drifting = unit_vector(wheel.angle, actual_wheel_speed * copysign(1, cos_angle)).distance_to(wheel.velocity)
            
            def inc_velocity(acceleration):
                if wheel.velocity.length() < abs(self._wheel_speed):
                    wheel.velocity += min(abs(self._wheel_speed) - wheel.velocity.length(), acceleration) * unit_vector(wheel.angle) * dt
                print(wheel.velocity.length())
            
            if self._braking or drifting > get_env("DRIFT_TRESHOLD"):
                self._color = (255, 0, 0)
                wheel.velocity *= (0.7 * abs(cos_angle)) ** dt
                #inc_velocity(self._acceleration / 2)
                
                wheel.position += lerp(wheel.velocity, projection, 0.8) * dt
                
            else:
                wheel.velocity *= (0.94 * (1 - (1 - abs(cos_angle)) ** 4)) ** dt
                #TODO AJOUTER DE LA PROJECTION A LA VELOCITE
                inc_velocity(self._acceleration)
                
                wheel.position += projection * dt

    def tick(self, dt):
        self._accelerate(dt)
        
        wheels_pre_fabrik = [w.position for w in self._wheels]
        
        reconstruct_car(self._wheels, self._width, self._length)
        self._wheels[2].angle += self._steer_angle
        self._wheels[3].angle += self._steer_angle
        if self._wheel_speed < 0:
            for wheel in self._wheels:
                wheel.angle = nice_angle(wheel.angle + pi)
        
        for i in range(4):
            wheel = self._wheels[i]
            wheel.velocity += (wheel.position - wheels_pre_fabrik[i]) / 1
    
    model = property_get("model")
    color = property_get("color")
    wheel_speed = property_getset("wheel_speed")
    steer_angle = property_getset("steer_angle")
    braking = property_getset("braking")

    def get_actual_front_wheels_speed(self):
        return lerp(self._wheels[0].velocity.length() * copysign(1, self._wheel_speed), self._wheels[1].velocity.length() * copysign(1, self._wheel_speed), 0.5)
    

class Wheel:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.last_position = position
        self.velocity = Vector2(0, 0)


class CarModel:
    def __init__(self, name, hitbox: tuple[int, int], weight, default_color):
        self._name = name
        self._default_color = default_color
        self._hitbox = hitbox
        self._weight = weight

    name = property_get("name")
    weight = property_get("weight")
    default_color = property_get("default_color")
    hitbox = property_get("hitbox")
