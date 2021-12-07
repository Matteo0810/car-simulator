from math import *

from engine.physics import reconstruct_car
from helpers.dotenv import get_env
from helpers.utils import *

import pygame.draw
from helpers.vector import Vector2


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
            
            drifting = Vector2.of_angle(wheel.angle, wheel.actual_speed).distance(wheel.velocity)
            
            def inc_velocity(acceleration):
                if wheel.actual_speed * sign(self._wheel_speed) < abs(self._wheel_speed):
                    actual_acceleration = min(self._wheel_speed - wheel.actual_speed
                                              , acceleration * sign(self._wheel_speed)
                                              , key=lambda x: sign(self._wheel_speed) * x)
                    wheel.velocity += actual_acceleration * Vector2.of_angle(wheel.angle) * dt

            inc_velocity(self._acceleration)
            projection = Vector2.of_angle(wheel.angle, wheel.actual_speed)
            
            if self._braking or drifting > get_env("DRIFT_TRESHOLD"):
                self._color = (255, 0, 0)
                wheel.velocity *= 0.8 ** dt
            else:
                wheel.velocity = projection
            
            wheel.position += wheel.velocity * dt
            
            rotation_speed_loss = abs(cos(wheel.velocity.angle() - wheel.angle))
            if wheel.actual_speed != 0:
                wheel.velocity *= (0.9 * rotation_speed_loss) ** dt
                wheel.velocity -= wheel.velocity.normalize() * dt * 5
     
    def tick(self, dt):
        self._accelerate(dt)
        
        wheels_pre_fabrik = [w.position for w in self._wheels]
        
        reconstruct_car(self._wheels, self._width, self._length)
        self._wheels[2].angle += self._steer_angle
        self._wheels[3].angle += self._steer_angle
        
        for i in range(4):
            wheel = self._wheels[i]
            wheel.velocity += (wheel.position - wheels_pre_fabrik[i]) / 1
    
    model = property_get("model")
    color = property_get("color")
    wheel_speed = property_getset("wheel_speed")
    steer_angle = property_getset("steer_angle")
    braking = property_getset("braking")

    def get_actual_front_wheels_speed(self):
        return lerp(self._wheels[0].actual_speed, self._wheels[1].actual_speed, 0.5)
    
    def get_center_of_mass(self):
        return sum((w.position for w in self._wheels), Vector2(0, 0)) / 4


class Wheel:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.last_position = position
        self.velocity = Vector2(0, 0)
    
    @property
    def actual_speed(self):
        return cos(self.velocity.angle() - self.angle) * self.velocity.length()


class CarModel:
    def __init__(self, name, hitbox: tuple, weight, default_color):
        self._name = name
        self._default_color = default_color
        self._hitbox = hitbox
        self._weight = weight

    name = property_get("name")
    weight = property_get("weight")
    default_color = property_get("default_color")
    hitbox = property_get("hitbox")
