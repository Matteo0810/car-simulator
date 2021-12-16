from math import *

import pygame

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


def _normal(p0, v0, p1, v1, p2, v2, screen):
    """
        Retourne le vecteur normal au segment [p1, p2] s'il y a intersection avec [p0, p0+v]
        Retourne None s'il n'y a pas d'intersection
    """

    cp1 = p1 - p0
    cp2 = p2 - p0
    cv1 = v1 - v0
    cv2 = v2 - v0
    
    try:
        t = - (cp1.x * (cp2.y - cp1.y) + cp1.y * (cp1.x - cp1.x)) / (cp1.x * (cv2.y - cv1.y) + cp1.y * (cv1.x - cv1.x))
        
        intersection = p0 + v0 * t
        pygame.draw.rect(screen, (0, 0, 255), pygame.rect.Rect(tuple(Vector2(350, 250)), (2, 2)))
        
        segment_length = p1.distance(p2)
        if intersection.distance(p2) < segment_length \
            and intersection.distance(p1) < segment_length \
            and intersection.distance(p0) < v0.length():
            
            normal = Vector2(-(p2.y - p1.y), p2.x - p1.x)
            u = p0 - intersection
            if normal.dot(u) < 0:
                return intersection, -normal.normalize()
            return intersection, normal.normalize()
    except ZeroDivisionError:
        pass
    return None, None


def check_collision(car1, car2, dt, screen):
    nearest_col = None
    for wheel0 in car1.wheels:
        for wheel1, wheel2 in [(car2.wheels[0], car2.wheels[1]), (car2.wheels[1], car2.wheels[2]), (car2.wheels[2], car2.wheels[3]), (car2.wheels[3], car2.wheels[0])]:
            intersection, normal = _normal(wheel0.position, wheel0.velocity * dt, wheel1.position, wheel1.velocity * dt, wheel2.position, wheel2.velocity * dt, screen)
            if normal:
                if not nearest_col or wheel0.position.distance(intersection) < nearest_col[0]:
                    nearest_col = (wheel0.position.distance(intersection), wheel0, wheel1, wheel2, normal)
    
    if nearest_col:
        nearest_col[1].velocity = nearest_col[4] * 50
        nearest_col[2].velocity = nearest_col[4] * -25
        nearest_col[3].velocity = nearest_col[4] * -25
