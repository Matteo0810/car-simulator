from math import *

from engine.model.model import Model
from engine.model.modeled import Modeled
from helpers.physics import reconstruct_car
from helpers.utils import *
from helpers.vector import Vector2


class Car(Modeled):
    def __init__(self, world, position, angle, car_type, ai=None):
        if car_type.model:
            super().__init__(Model.load(car_type.model))
        else:
            super().__init__(None)

        self._wheels = [Wheel(Vector2(0, 0), 0) for _ in range(4)]
        self._car_type = car_type
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
            if wheel.drifting:
                print("drifting:", True)

            if not wheel.drifting:
                wheel.drifting = False and slipping.length() > 10 / (1 - ground.grip)
            else:
                wheel.drifting = slipping.length() > 9 / (1 - ground.grip)

            if not braking and wheel.actual_speed * sign(target_speed) < abs(target_speed):
                actual_acceleration = min(target_speed - wheel.actual_speed,
                                          self._car_type.acceleration * sign(target_speed),
                                          key=lambda x: sign(target_speed) * x) * (
                                          ground.grip * 0.6 if wheel.drifting else ground.grip)
                wheel.velocity += actual_acceleration * Vector2.of_angle(wheel.angle) * dt

            if braking:
                wheel.velocity *= 0.25 ** dt

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

            # engine.debug.scene2d.INSTANCE.add_debug_dot(wheel.position + wheel.velocity, (0, 255, 0))

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
    car_type = property_get("car_type")
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
