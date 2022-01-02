from engine.model.modeled import Modeled

from engine.physics import reconstruct_car

from helpers.utils import *
from helpers.vector import Vector2


class Car(Modeled):
    def __init__(self, position, angle, car_type, ai):
        super().__init__(car_type.model)
        
        self._wheels = [Wheel(Vector2(0, 0), 0) for _ in range(4)]
        self._model = car_type
        self._width = width = car_type.width
        self._length = length = car_type.length
        self._color = car_type.default_color
        self.ai = ai

        front_angle = atan2(width, length)
        diagonal = (width ** 2 + length ** 2) ** 0.5

        wheel_angles = [
            nice_angle(front_angle + pi),
            nice_angle(-front_angle + pi),
            nice_angle(front_angle),
            nice_angle(-front_angle)
        ]

        for i in range(4):
            self._wheels[i].position = position + Vector2.of_angle(wheel_angles[i] + angle) * diagonal / 2
            self._wheels[i].last_position = self._wheels[i].position
            self._wheels[i].angle = angle
    
    def _accelerate(self, world, dt, target_speed, braking):
        for wheel in self._wheels:
            ground = world.get_ground_at(wheel.position)
            
            drifting = Vector2.of_angle(wheel.angle, wheel.actual_speed).distance(wheel.velocity) > ground.grip \
                    or braking
            
            if not drifting and wheel.actual_speed * sign(target_speed) < abs(target_speed):
                actual_acceleration = min(target_speed - wheel.actual_speed,
                                          self._model.acceleration * sign(target_speed),
                                          key=lambda x: sign(target_speed) * x)
                wheel.velocity += actual_acceleration * Vector2.of_angle(wheel.angle) * dt

            projection = Vector2.of_angle(wheel.angle, wheel.actual_speed)
            
            if drifting:
                wheel.velocity -= wheel.velocity.normalize() * dt * 5
                wheel.velocity = lerp(projection, wheel.velocity, dt)
            else:
                wheel.velocity = projection

            rotation_speed_loss = abs(cos(wheel.velocity.angle() - wheel.angle))
            if wheel.actual_speed != 0:
                wheel.velocity *= rotation_speed_loss ** dt
                wheel.velocity -= wheel.velocity.normalize() * dt * ground.friction_loss

    def tick(self, world, dt):
        target_speed = self.ai.get_wheel_speed(world, self)
        steer_angle = self.ai.get_steer_angle(world, self)
        braking = self.ai.is_braking(world, self)

        self._wheels[2].angle += steer_angle
        self._wheels[3].angle += steer_angle
        self._accelerate(world, dt, target_speed, braking)
        
        for wheel in self._wheels:
            wheel.position += wheel.velocity * dt
        
        self.reconstruct()
    
    def reconstruct(self):
        wheels_pre_fabrik = [w.position for w in self._wheels]
        
        reconstruct_car(self._wheels, self._width, self._length)
        
        for i in range(4):
            wheel = self._wheels[i]
            wheel.velocity += (wheel.position - wheels_pre_fabrik[i]) / 1
    
    def update_last_position(self, world, dt):
        for wheel in self._wheels:
            wheel.last_position = Vector2(*wheel.position)
    
    model = property_get("model")
    color = property_get("color")
    steer_angle = property_getset("steer_angle")
    braking = property_getset("braking")

    def get_actual_front_wheels_speed(self):
        return lerp(self._wheels[2].actual_speed, self._wheels[3].actual_speed, 0.5)

    def get_actual_back_wheels_speed(self):
        return lerp(self._wheels[0].actual_speed, self._wheels[1].actual_speed, 0.5)
    
    @property
    def wheels(self):
        return self._wheels[:]


class Wheel:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.last_position = position
        self.velocity = Vector2(0, 0)

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
