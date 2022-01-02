from abc import ABC, abstractmethod
from math import copysign
from random import choice

from helpers.vector import Vector2
from world.car import Car


class AI(ABC):
    @abstractmethod
    def get_wheel_speed(self):
        pass
    
    @abstractmethod
    def get_steer_angle(self):
        pass
    
    @abstractmethod
    def is_braking(self):
        pass
    
    # pas une méthode abstraite !
    def pre_tick(self, dt):
        pass


def unpack_actions_flag(actions_flag, speed_limit):
    if actions_flag & 0b11100 == 0b00000:
        steer_angle = -1
    elif actions_flag & 0b11100 == 0b00100:
        steer_angle = -0.3
    elif actions_flag & 0b11100 == 0b01000:
        steer_angle = 1
    elif actions_flag & 0b11100 == 0b01100:
        steer_angle = 0.3
    else:
        steer_angle = 0
    
    if actions_flag & 0b11 != 0b11:
        braking = False
        if actions_flag & 0b11 == 0b01:
            wheel_speed = -speed_limit / 2
        elif actions_flag & 0b11 == 0b10:
            wheel_speed = speed_limit
        else:
            wheel_speed = 0
    else:
        wheel_speed = 0
        braking = True
    
    return steer_angle, wheel_speed, braking


TIME_STEP = 0.5
FORESEE_TIME = 3


class AIImpl(AI):
    def __init__(self, path, car):
        self._path = path
        self._next_path = None
        self._car = car
        self._t = 0
        self._wheel_speed = 0
        self._braking = False
        self._steer_angle = 0
        self._last_steer_angle = 0
        self._dt = 0
        self._actions = []
    
    def get_wheel_speed(self):
        return self._wheel_speed
    
    def get_steer_angle(self):
        self._last_steer_angle = self._steer_angle if self._steer_angle - self._last_steer_angle < self._dt else copysign(self._dt, self._steer_angle - self._last_steer_angle) + self._last_steer_angle
        return self._last_steer_angle
    
    def is_braking(self):
        return self._braking
    
    def pre_tick(self, dt):
        self._dt = dt
        self._t += dt
        
        if self._car.position.distance(self._path.end) < 4:
            self._path = self._next_path
            self._next_path = None
        
        if self._next_path is None:
            self._next_path = choice(self._path.intersection.inbounds).path
            print(self._next_path, self._next_path.intersection)
        
        if len(self._actions) > 0:
            if self._t >= TIME_STEP:
                self._steer_angle, self._wheel_speed, self._braking = unpack_actions_flag(self._actions.pop(0),
                                                                                          self._path.road.speed_limit)
                self._steer_angle *= 5 / max(5, abs(self._car.get_actual_front_wheels_speed()))
                self._t -= TIME_STEP
            
        else:
            self._wheel_speed = 0
            self._braking = False
            self._steer_angle = 0

    def pathfinding(self, scene):
        car = self._car
    
        nodes = [{"parent": None, "score": 0, "actions_flag": 0, "time": 0,
                  "car_position": car.position, "car_velocity": car.velocity.length(), "car_angle": car.angle}]
    
        # chaque noeud (ou instant) posséde un score basé sur la distance
        # à la route, l'avancée sur la route et la proximité des obstacles dangereux à court terme
    
        # les noeuds sont caractérisés par un choix (flag) du format suivant:
        # 2 premiers bits: choix d'accélération (00: laisser rouler, 01: reculer, 10: avancer, 11: freiner)
        # 3 bits suivants: choix de direction (100: avant, 000: gauche (bcp), 001: gauche (un peu),
        # 010: droite (bcp), 011: droite (un peu))
        loops = 0
    
        # simulation rapide du déplacement de la voiture et de son environnement
        while True:
            loops += 1
            parent = max([n for n in nodes], key=lambda node: node["score"])
            # print(parent)
            nodes.remove(parent)
        
            if parent["time"] == FORESEE_TIME:
                self._actions = []
            
                while parent["parent"]["parent"]:
                    self._actions.append(parent["actions_flag"])
                    parent = parent["parent"]
                    scene.add_debug_dot(parent["car_position"])
            
                self._actions.append(parent["actions_flag"])
                self._actions.reverse()
                return
        
            children = []
        
            for actions_flag in range(0b10001):
                node = {"parent": parent, "actions_flag": actions_flag, "time": parent["time"] + TIME_STEP}
                score = 0
            
                position = parent["car_position"]
                velocity = parent["car_velocity"]
                angle = parent["car_angle"]
            
                steer_angle, wheel_speed, braking = unpack_actions_flag(actions_flag, 1)
            
                if wheel_speed > 0:
                    velocity += car.model.acceleration * TIME_STEP
                if wheel_speed < 0:
                    velocity -= car.model.acceleration * TIME_STEP
            
                if abs(velocity) < 7:
                    angle += steer_angle * TIME_STEP * velocity/7
                else:
                    angle += steer_angle * TIME_STEP * copysign(1, velocity)
            
                position += Vector2.of_angle(angle, velocity) * TIME_STEP
            
                for collideable in car.world.collideables:
                    if collideable == car:
                        continue
                
                    nearest_hitbox_point = collideable.nearest_hitbox_point(position)
                
                    if isinstance(collideable, Car):
                        nearest_hitbox_point += collideable.velocity * (parent["time"] + TIME_STEP)
                
                    if nearest_hitbox_point and nearest_hitbox_point.distance(position) < car.model.diagonal:
                        score -= (car.model.diagonal - nearest_hitbox_point.distance(
                            position)) * self._path.start.distance(self._path.end) * 100
            
                score -= self._path.distance(position) ** 2
                score -= self._path.end.distance(position)
            
                # print()
                # print(copysign(1, wheel_speed) if wheel_speed != 0 else 0, steer_angle, braking)
                # print(self._path.distance(position) ** 2)
                # print(self._path.end.distance(position))
                # print(score)
            
                node["score"] = score
                node["car_position"] = position
                node["car_velocity"] = velocity
                node["car_angle"] = angle
                children.append(node)
        
            nodes.extend(children)

"""
for t in (i * time_step for i in range(1, int(foresee_time / time_step))):
    for car1 in car.world.cars:
        if car1 == car:
            continue

        if (car.position + t * car.velocity).distance(car1.position + t * car1.velocity) < (max(car.model.width, car.model.length) + max(car1.model.width, car1.model.length))/2 + 1.5:
            self._wheel_speed = 0
            if t < 1:
                self._braking = True"""
