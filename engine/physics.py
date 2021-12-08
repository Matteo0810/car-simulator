from math import *
from helpers.vector import Vector2
from helpers.utils import *


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
            car_angles.append((wheels[i].position - center_of_mass).angle() - wheel_angles[i])
        
        mean_angle = atan2(sum((sin(a) for a in car_angles)), sum((cos(a) for a in car_angles)))
    else:
        mean_angle = hard_angle
    
    for i in range(4):
        wheels[i].position = center_of_mass + Vector2.of_angle(wheel_angles[i] + mean_angle) * diagonal / 2
        wheels[i].angle = mean_angle
