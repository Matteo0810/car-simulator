import threading
from abc import ABC, abstractmethod
from random import choice

from helpers.dotenv import get_env
from helpers.ordered_list import OrderedList
from helpers.vector import Vector2
from helpers.utils import sign
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


class DefinedAI(AI):
    def __init__(self, car):
        self._car = car
        self.wheel_speed = 0
        self.braking = False
        self.steer_angle = 0
    
    def get_wheel_speed(self):
        return self.wheel_speed * 5 / max(5, abs(self._car.get_actual_front_wheels_speed()))
    
    def get_steer_angle(self):
        return self.steer_angle
    
    def is_braking(self):
        return self.braking


def unpack_actions_flag(actions_flag, speed_limit):
    if actions_flag & 0b11100 == 0b00000:
        steer_angle = -0.6
    elif actions_flag & 0b11100 == 0b00100:
        steer_angle = -0.3
    elif actions_flag & 0b11100 == 0b01000:
        steer_angle = -0.1
    elif actions_flag & 0b11100 == 0b01100:
        steer_angle = 0.6
    elif actions_flag & 0b11100 == 0b10000:
        steer_angle = 0.3
    elif actions_flag & 0b11100 == 0b10100:
        steer_angle = 0.1
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
FORESEE_TIME = 2


class AIImpl(AI):
    def __init__(self, path, car):
        self._path = path
        
        self._next_path = None
        self._choose_next_path()
        
        self._car = car
        self._t = 0
        self._wheel_speed = 0
        self._braking = False
        self._steer_angle = 0
        self._dt = 0
        self._actions = []
        self._current_action = None
        self._action_changed = False
        self._lock = threading.Lock()
    
    def get_wheel_speed(self):
        return self._wheel_speed * 5 / max(5, abs(self._car.get_actual_front_wheels_speed()))
    
    def get_steer_angle(self):
        return self._steer_angle
    
    def is_braking(self):
        return self._braking
    
    def _choose_next_path(self):
        self._next_path = choice(self._path.intersection.outbounds)
        while self._next_path.road == self._path.road and any(p.road != self._path.road for p in self._path.intersection.outbounds):
            self._next_path = choice(self._path.intersection.outbounds)
    
    def pre_tick(self, dt):
        self._dt = dt
        self._t += dt

        self._lock.acquire()
        
        has_priority = self._path.intersection.has_priority(self._path, self._next_path, self._car.world)
        
        if self._car.position.distance(self._path.end) < 10 and has_priority or self._car.position.distance(self._path.end) < 5:
            self._path = self._next_path
            self._next_path = None
        
        if self._next_path is None:
            self._choose_next_path()
        
        if len(self._actions) > 0:
            if self._t >= TIME_STEP or self._action_changed:
                self._action_changed = False
                
                self._current_action = self._actions.pop(0)
                
                self._steer_angle, self._wheel_speed, self._braking = unpack_actions_flag(self._current_action["actions_flag"],
                                                                                          self._path.road.speed_limit)
                self._t %= TIME_STEP
            
        else:
            self._wheel_speed = 0
            self._braking = True
            self._steer_angle = 0
        
        self._lock.release()

    def pathfinding(self, scene):
        car = self._car

        self._lock.acquire()
        
        next_path = self._next_path
        current_path = self._path
        
        has_priority = current_path.intersection.has_priority(current_path, next_path, self._car.world)
        
        node_source = {"parent": None, "score": 0, "actions_flag": 0, "time": 0, "on_next_path": False, "changed_path": False,
                  "car_position": car.position, "car_velocity": car.velocity.length(), "car_angle": car.angle}
        
        start_pos = car.position
        
        self._lock.release()
        
        node_value = lambda node: node["score"]# + node["dev_score"]
        
        nodes = OrderedList(lambda n1, n2: node_value(n1) - node_value(n2), [node_source])
        
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
            
            parent = nodes.min()
        
            if loops > 20 or parent["time"] == FORESEE_TIME:
                
                self._lock.acquire()
                
                self._actions = []
                while parent["parent"]["parent"]:
                    self._actions.append(parent)
                    parent = parent["parent"]
                    #scene.add_debug_dot(parent["car_position"], (200, 200, 0))
                
                self._actions.append(parent)
                self._actions.reverse()
                
                self._lock.release()
                
                self._action_changed = True
                return
            
            nodes.remove(parent)
        
            for actions_flag in range(0b11001):
                #if actions_flag & 0b11 == 0b11:
                #    continue
                
                node = {"parent": parent, "actions_flag": actions_flag, "time": parent["time"] + TIME_STEP}
                score = 0
                
                position = parent["car_position"]
                velocity = parent["car_velocity"]
                angle = parent["car_angle"]
                path = next_path if parent["on_next_path"] else current_path
                
                steer_angle, wheel_speed, braking = unpack_actions_flag(actions_flag, path.road.speed_limit)
                vel_diff = 0
                
                if braking:
                    vel_diff = -velocity * 0.5
                else:
                    if wheel_speed > 0 and velocity < path.road.speed_limit:
                        if sign(velocity) != sign(wheel_speed):
                            vel_diff = car.model.acceleration * TIME_STEP
                        else:
                            vel_diff = car.model.acceleration * TIME_STEP
                    if wheel_speed < 0 and velocity > -path.road.speed_limit:
                        if sign(velocity) != sign(wheel_speed):
                            vel_diff = -car.model.acceleration * TIME_STEP
                        else:
                            vel_diff = -car.model.acceleration * TIME_STEP
                
                #B, C, D, E = 0.01, 1.7, -100, -1.2
                #x = (velocity + vel_diff) * 25
                #f = D * sin(C * atan(B * x/2 - E * (B * x/2 - atan(B * x/2))))
                #angle -= f * steer_angle / 150 * sign(velocity) * 1.5
                angle += velocity * steer_angle * TIME_STEP / 7
                
                velocity += vel_diff - 2 * sign(velocity)
                
                l_position = position
                position += Vector2.of_angle(angle, velocity) * TIME_STEP
                
                node["on_next_path"] = (parent["on_next_path"] or path.end.distance(position) < 5) and has_priority
                node["changed_path"] = not parent["on_next_path"] and node["on_next_path"]
                
                path = next_path if node["on_next_path"] else current_path
                
                if not node["changed_path"] and not parent["changed_path"]:
                    score += path.distance(position)
                else:
                    score += path.distance(position)
                
                if not has_priority:
                    goal = (path.end - path.direction * get_env("ROAD_WIDTH") * 0.8)
                    score += goal.distance(position)
                    if goal.distance(position) < goal.distance(position + Vector2.of_angle(angle, velocity) / 2):
                        score += velocity
                else:
                    score += path.end.distance(position)
                
                if not node["on_next_path"]:
                    score += current_path.end.distance(next_path.end)
                
                for collideable in car.world.collideables:
                    if collideable == car:
                        continue
                
                    nearest_hitbox_point = collideable.nearest_hitbox_point(position)
                    
                    if nearest_hitbox_point:
                        if isinstance(collideable, Car):
                            nearest_hitbox_point += collideable.velocity * node["time"]
                        
                        dist = nearest_hitbox_point.distance(position)
                        
                        if dist <= car.model.diagonal and node["time"] < 1:
                            score += 10000000
                        #if dist <= car.model.diagonal:
                        #    score += (car.model.diagonal - dist)
                
                node["score"] = score
                node["car_position"] = position
                node["car_velocity"] = velocity
                node["car_angle"] = angle
                nodes.insert(node)
