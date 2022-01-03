from engine.model.modeled import Modeled

from engine.physics import reconstruct_car

from helpers.utils import *
from helpers.vector import Vector2

A = {}


class Car(Modeled):
    def __init__(self, world, position, angle, car_type, ai=None):
        super().__init__(car_type.model)
        
        self._wheels = [Wheel(Vector2(0, 0), 0) for _ in range(4)]
        self._model = car_type
        self._width = width = car_type.width
        self._length = length = car_type.length
        self._color = car_type.default_color
        self._world = world
        self._angle = angle
        self.ai = ai

        front_angle = atan2(width, length)

        wheel_angles = [
            nice_angle(front_angle + pi),
            nice_angle(-front_angle + pi),
            nice_angle(front_angle),
            nice_angle(-front_angle)
        ]

        for i in range(4):
            self._wheels[i].position = position + Vector2.of_angle(wheel_angles[i] + angle) * car_type.diagonal / 2
            self._wheels[i].last_position = self._wheels[i].position
            self._wheels[i].angle = angle
    
    def _accelerate(self, dt, target_speed, braking):
        for wheel in self._wheels:
            ground = self._world.get_ground_at(wheel.position)
            
            slipping = wheel.velocity - Vector2.of_angle(wheel.angle, wheel.actual_speed)
            
            if not wheel.drifting:
                wheel.drifting = slipping.length() > 10
            else:
                wheel.drifting = slipping.length() > 9
            
            if wheel.actual_speed * sign(target_speed) < abs(target_speed):
                actual_acceleration = min(target_speed - wheel.actual_speed,
                                          self._model.acceleration * sign(target_speed),
                                          key=lambda x: sign(target_speed) * x) * (ground.grip*0.6 if wheel.drifting else ground.grip)
                wheel.velocity += actual_acceleration * Vector2.of_angle(wheel.angle) * dt

            projection = Vector2.of_angle(wheel.angle, wheel.actual_speed)
            
            if wheel.drifting:
                wheel.velocity *= 0.9 ** dt
            else:
                wheel.velocity = projection

            rotation_speed_loss = abs(cos(wheel.velocity.angle() - wheel.angle))
            if wheel.actual_speed != 0:
                wheel.velocity *= rotation_speed_loss ** dt * 0.9 ** dt
                if dt * ground.friction_loss <= wheel.velocity.length():
                    wheel.velocity -= wheel.velocity.normalize() * dt * ground.friction_loss

    def tick(self, dt):
        last_angle = self.angle
        if self.ai:
            target_speed = self.ai.get_wheel_speed()
            steer_angle = self.ai.get_steer_angle()
            braking = self.ai.is_braking()
        else:
            target_speed = 0
            steer_angle = 0
            braking = False

        self._wheels[2].angle += steer_angle
        self._wheels[3].angle += steer_angle
        self._accelerate(dt, target_speed, braking)
        
        for wheel in self._wheels:
            wheel.position += wheel.velocity * dt
        
        self.reconstruct()
        
        if steer_angle > 0:
            A[self.velocity.length()] = (self.angle - last_angle) / dt
            #print((self.angle - last_angle) / dt)
    
    def reconstruct(self):
        wheels_pre_fabrik = [w.position for w in self._wheels]
        
        self._angle = reconstruct_car(self._wheels, self._width, self._length)
        
        for i in range(4):
            wheel = self._wheels[i]
            wheel.velocity += (wheel.position - wheels_pre_fabrik[i]) / 1
    
    def update_last_position(self, dt):
        for wheel in self._wheels:
            wheel.last_position = Vector2(*wheel.position)

    world = property_get("world")
    model = property_get("model")
    color = property_get("color")
    steer_angle = property_getset("steer_angle")
    braking = property_getset("braking")

    def get_actual_front_wheels_speed(self):
        return lerp(self._wheels[2].actual_speed, self._wheels[3].actual_speed, 0.5)

    def get_actual_back_wheels_speed(self):
        return lerp(self._wheels[0].actual_speed, self._wheels[1].actual_speed, 0.5)
    
    @property
    def velocity(self):
        return sum(w.velocity for w in self._wheels) / 4
    
    @property
    def position(self):
        return sum(w.position for w in self._wheels) / 4
    
    @property
    def angle(self):
        return self._angle
    
    @property
    def wheels(self):
        return self._wheels[:]
    
    @property
    def hitbox(self):
        return [wheel.position for wheel in self._wheels]


class Wheel:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.last_position = position
        self.velocity = Vector2(0, 0)
        self.drifting = False

    @property
    def actual_speed(self):
        return cos(self.velocity.angle() - self.angle) * self.velocity.length()


class CarType:
    def __init__(self, model, width, length, weight, default_color, acceleration):
        self._model = model
        self._default_color = default_color
        self._width = width
        self._length = length
        self._weight = weight
        self._acceleration = acceleration

    model = property_get("model")
    weight = property_get("weight")
    default_color = property_get("default_color")
    width = property_get("width")
    length = property_get("length")
    acceleration = property_get("acceleration")
    
    @property
    def diagonal(self):
        return (self.width ** 2 + self.length ** 2) ** 0.5
