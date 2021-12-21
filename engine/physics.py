from math import *

import pygame

from helpers.vector import Vector2
from helpers.utils import *
from helpers.dotenv import get_env


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


def _solve_quadratic(a, b, c):
    """
        retourne les solutions de l'équation a*x*x + b*x + c = 0
    """
    if a == 0:
        if b == 0:
            return ()
        return -c / b,
    
    delta = b * b - 4 * a * c
    if delta > 0:
        return (-b - sqrt(delta)) / (2 * a), (-b + sqrt(delta)) / (2 * a)
    elif delta == 0:
        return -b / (2 * a),
    else:
        return ()


def _normal(p0, v0, p1, v1, p2, v2):
    """
        Retourne le vecteur normal au segment [p1, p2] s'il y a intersection avec [p0, p0+v]
        Retourne None s'il n'y a pas d'intersection
    """

    cp1 = p1 - p0
    cp2 = p2 - p0
    cv1 = v1 - v0
    cv2 = v2 - v0
    
    a = cv1.y * cv2.x - cv1.x * cv2.y
    b = cv1.y * cp2.x + cp1.y * cv2.x - cv1.x * cp2.y - cp1.x * cv2.y
    c = cp1.y * cp2.x - cp1.x * cp2.y
    
    solutions = _solve_quadratic(a, b, c)
    t_index = -1
    
    for i in range(len(solutions)):
        if 0 <= solutions[i] < 1 and (t_index == -1 or solutions[i] < solutions[t_index]):
            t_index = i
    
    if t_index == -1:
        return None, None, 0
    
    t = solutions[t_index]
    
    intersection = p0 + v0 * t
    #pygame.draw.rect(screen, (0, 0, 255), pygame.rect.Rect(tuple(Vector2(get_env("WIDTH") / 2, get_env("HEIGHT") / 2)), (2, 2)))
    
    segment_length = (p1 + t * v1).distance(p2 + t * v2)
    if intersection.distance(p2 + t * v2) <= segment_length \
            and intersection.distance(p1 + t * v1) <= segment_length:
        
        normal = Vector2(-(p2.y + v2.y - p1.y - v1.y), p2.x + v2.x - p1.x - v1.x)
        u = p0 - intersection
        if normal.dot(u) < 0:
            return intersection, normal.normalize(), t
        return intersection, normal.normalize(), t
    return None, None, 0


def check_collision(car1, car2, dt):
    collisions = []
    
    for wheel0 in car1.wheels:
        for wheel1, wheel2 in [(car2.wheels[0], car2.wheels[1]), (car2.wheels[1], car2.wheels[2]), (car2.wheels[2], car2.wheels[3]), (car2.wheels[3], car2.wheels[0])]:
            args = []
            for w in (wheel0, wheel1, wheel2):
                args.append(w.last_position)
                args.append(w.position - w.last_position)
            
            collision, normal, t = _normal(*args)
            
            if normal:
                collisions.append((wheel0, wheel1, wheel2, collision, normal, t))
                rel_hit_pos = wheel2.position.distance(collision) / wheel1.position.distance(wheel2.position)
                
                f0 = wheel0.velocity
                f1 = lerp(wheel1.velocity, wheel2.velocity, 1 - rel_hit_pos)
                f = f0 + f1
                
                wheel0.velocity = normal * f.length()*2
                wheel0.position = collision + wheel0.velocity * dt
                
                wheel1.velocity = lerp(normal * -f.length()*2, wheel1.velocity, rel_hit_pos)
                wheel2.velocity = lerp(normal * -f.length()*2, wheel2.velocity, 1 - rel_hit_pos)
                
                wheel1.position = lerp(wheel1.last_position, wheel1.position, t)
                wheel2.position = lerp(wheel2.last_position, wheel2.position, t)
    
    """for acollision in sorted(collisions, key=lambda l: l[5]):
        wheel0, wheel1, wheel2, collision, normal, t = acollision
        rel_hit_pos = wheel2.position.distance(collision) / wheel1.position.distance(wheel2.position)
        
        f0 = wheel0.velocity
        f1 = lerp(wheel1.velocity, wheel2.velocity, 1 - rel_hit_pos)
        f = f0 + f1
        
        wheel0.velocity = normal * f.length()
        wheel0.position = collision
        
        wheel1.velocity = lerp(normal * -f.length(), wheel1.velocity, rel_hit_pos)
        wheel2.velocity = lerp(normal * -f.length(), wheel2.velocity, 1 - rel_hit_pos)
        
        wheel1.position = wheel1.last_position
        wheel2.position = wheel2.last_position"""
