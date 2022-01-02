from math import *

from helpers.vector import Vector2
from helpers.utils import *


def reconstruct_car(wheels, car_width, car_length):
    front_angle = atan2(car_width, car_length)
    diagonal = sqrt(car_width ** 2 + car_length ** 2)
    
    wheel_angles = [
        nice_angle(front_angle + pi),
        nice_angle(-front_angle + pi),
        nice_angle(front_angle),
        nice_angle(-front_angle)
    ]
    
    center_of_mass = sum((w.position for w in wheels), Vector2(0, 0)) / 4
    
    car_angles = []
    for i in range(4):
        car_angles.append((wheels[i].position - center_of_mass).angle() - wheel_angles[i])
    
    mean_angle = atan2(sum((sin(a) for a in car_angles)), sum((cos(a) for a in car_angles)))
    
    for i in range(4):
        wheels[i].position = center_of_mass + Vector2.of_angle(wheel_angles[i] + mean_angle) * diagonal / 2
        wheels[i].angle = mean_angle


ALL_REALS = "ALL_REALS"


def _solve_quadratic(a, b, c) -> tuple:
    """
        retourne les solutions de l'équation a*x*x + b*x + c = 0
    """
    if a == 0:
        if b == 0:
            if c == 0:
                return ALL_REALS
            return ()
        return -c / b,
    
    delta = b * b - 4 * a * c
    if delta > 0:
        return (-b - sqrt(delta)) / (2 * a), (-b + sqrt(delta)) / (2 * a)
    elif delta == 0:
        return -b / (2 * a),
    else:
        return ()


def _normal(p0, v0, p1, v1, p2, v2, p=False):
    cp1 = p1 - p0
    cp2 = p2 - p0
    cv1 = v1 - v0
    cv2 = v2 - v0
    
    a = cv1.y * cv2.x - cv1.x * cv2.y
    b = cv1.y * cp2.x + cp1.y * cv2.x - cv1.x * cp2.y - cp1.x * cv2.y
    c = cp1.y * cp2.x - cp1.x * cp2.y
    
    solutions = _solve_quadratic(a, b, c)
    
    if p:
        print()
        print(p0, v0)
        print(p1, v1)
        print(p2, v2)
        print(a, b, c)
        print(solutions)
    
    if solutions == ALL_REALS:
        t = 0
    else:
        t_index = -1
        
        for i in range(len(solutions)):
            if 0 < solutions[i] < 1 and (t_index == -1 or solutions[i] < solutions[t_index]):
                t_index = i
        
        if t_index == -1:
            return None, None, 0
        
        t = solutions[t_index]
    
    intersection = p0 + v0 * t
    
    np1 = p1 + t * v1
    np2 = p2 + t * v2
    
    segment_length = np1.distance(np2)
    if intersection.distance(np2) <= segment_length \
            and intersection.distance(np1) <= segment_length:
        
        normal = Vector2(-(np2.y - np1.y), np2.x - np1.x)
        rel_pos = intersection.distance(np2) / np1.distance(np2)
        
        if normal.dot(v0 + p2 + (p1 - p2).normalize() * p2.distance(p1) * rel_pos - intersection) < 0:
            return intersection, normal.normalize(), t
        return intersection, -normal.normalize(), t
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
    
    for collision_ in collisions[:]:
        wheel0, wheel1, wheel2, collision, normal, t = collision_
        rel_hit_pos = wheel2.position.distance(collision) / wheel1.position.distance(wheel2.position)
        
        u1 = wheel0.velocity
        u2 = lerp(wheel1.velocity, wheel2.velocity, rel_hit_pos)
        
        r = 2
        
        wheel0.velocity += 2 * normal * abs(wheel0.velocity.dot(normal)) + u2 - u1
        wheel0.position = collision + normal / 2
        
        wheel1.velocity += lerp(-2 * normal * abs(wheel1.velocity.dot(normal)) + u1 - wheel1.velocity, 0, rel_hit_pos)
        wheel2.velocity += lerp(-2 * normal * abs(wheel2.velocity.dot(normal)) + u1 - wheel2.velocity, 0, 1 - rel_hit_pos)
        
        wheel1.position = lerp(wheel1.last_position, wheel1.position, t) - normal / 2
        wheel2.position = lerp(wheel2.last_position, wheel2.position, t) - normal / 2
