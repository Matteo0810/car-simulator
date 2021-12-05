from math import *
from pygame import Vector2


def unit_vector(angle: float, length: float = 1):
    return Vector2(cos(angle), sin(angle)) * length


def angle_of(vector: Vector2):
    return atan2(vector.y, vector.x)


def nice_angle(rad):
    return (rad + pi) % (2 * pi) - pi


def reconstruct_car(wheels, car_width, car_length, hard_position=None, hard_angle=None):
    front_angle = atan2(car_width, car_length)
    diagonal = sqrt(car_width ** 2 + car_length ** 2)
    
    wheel_angles = [
        nice_angle(front_angle + pi),
        nice_angle(-front_angle + pi),
        nice_angle(front_angle),
        nice_angle(-front_angle)
    ]
    
    center_of_mass = hard_position if hard_position else sum((w.position for w in wheels), Vector2(0, 0)) / 4
    
    if hard_angle is None:
        car_angles = []
        for i in range(4):
            car_angles.append(angle_of(wheels[i].position - center_of_mass) - wheel_angles[i])
        
        mean_angle = atan2(sum((sin(a) for a in car_angles)), sum((cos(a) for a in car_angles)))
    else:
        mean_angle = hard_angle
    
    for i in range(4):
        wheels[i].position = center_of_mass + unit_vector(wheel_angles[i] + mean_angle) * diagonal / 2
        wheels[i].angle = mean_angle
