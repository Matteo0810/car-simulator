from math import *

from engine.physics import reconstruct_car
from helpers.dotenv import get_env

import pygame.draw
from pygame import Vector2


def nice_angle(rad):
    return (rad + pi) % (2 * pi) - pi


def unit_vector(angle: float, length: float = 1):
    return Vector2(cos(angle), sin(angle)) * length


def angle_of(vector: Vector2):
    return atan2(vector.y, vector.x)


def lerp(a, b, m):
    return a * m + b * (1 - m)


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
        
        self._acceleration = 0.3
        
        reconstruct_car(self._wheels, width, length, hard_position=position, hard_angle=angle)
    
    def _accelerate(self, dt):
        self._color = (0, 255, 0)
        for wheel in self._wheels:
            wheel.last_position = wheel.position
        
            actual_wheel_speed = wheel.velocity.length()
        
            drifting = unit_vector(wheel.angle, actual_wheel_speed * copysign(1, self._wheel_speed)).distance_to(wheel.velocity)
        
            wheel.position += wheel.velocity * dt

            cos_angle = cos(unit_vector(wheel.angle).angle_to(wheel.velocity) / 180 * pi)
            projection = cos_angle * unit_vector(wheel.angle) * wheel.velocity.length()
            
            if self._braking or drifting > get_env("DRIFT_TRESHOLD"):
                self._color = (255, 0, 0)
                wheel.velocity *= (0.8 * abs(cos_angle)) ** dt
                wheel.velocity = lerp(wheel.velocity, unit_vector(wheel.angle) * self._wheel_speed,
                                      (1 - self._acceleration / 2) ** dt)
                
                wheel.position += lerp(wheel.velocity, projection, 0.8) * dt
            else:
                wheel.velocity *= (0.976 * abs(cos_angle)) ** dt
                wheel.velocity = lerp(wheel.velocity, unit_vector(wheel.angle) * self._wheel_speed,
                                      (1 - self._acceleration) ** dt)
                
                wheel.position += projection * dt

    def tick(self, dt):
        self._accelerate(dt)
        
        wheels_pre_fabrik = [w.position for w in self._wheels]
        
        reconstruct_car(self._wheels, self._width, self._length)
        self._wheels[2].angle += self._steer_angle
        self._wheels[3].angle += self._steer_angle
        
        for i in range(4):
            wheel = self._wheels[i]
            wheel.velocity += (wheel.position - wheels_pre_fabrik[i]) / 1
    
    @property
    def model(self):
        return self._model
    
    @property
    def color(self):
        return self._color
    
    @property
    def wheel_speed(self):
        return self._wheel_speed
    
    @wheel_speed.setter
    def wheel_speed(self, speed):
        self._wheel_speed = speed

    def get_actual_front_wheels_speed(self):
        return lerp(self._wheels[0].velocity.length() * copysign(1, self._wheel_speed), self._wheels[1].velocity.length() * copysign(1, self._wheel_speed), 0.5)
    
    @property
    def steer_angle(self):
        return self._steer_angle
    
    @steer_angle.setter
    def steer_angle(self, angle):
        self._steer_angle = angle

    @property
    def braking(self):
        return self._braking

    @braking.setter
    def braking(self, braking):
        self._braking = braking
    

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
    
    @property
    def name(self):
        return self._name
    
    @property
    def weight(self):
        return self._weight
    
    @property
    def default_color(self):
        return self._default_color
    
    @property
    def hitbox(self):
        return self._hitbox
