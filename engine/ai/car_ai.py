import threading
from abc import ABC, abstractmethod
from random import choice

from engine.ai.pathfinding import find_path, unpack_actions_flag
from engine.ai.pf_thread import PFThread


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
        self._my_thread = None
    
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
    
    @property
    def path(self):
        return self._path
    
    @property
    def next_path(self):
        return self._next_path
    
    def start_thread(self, scene):
        if not self._my_thread:
            self._my_thread = PFThread(self._car, scene)
            self._my_thread.start()
    
    def stop_thread(self):
        if self._my_thread:
            self._my_thread.stop()
            self._my_thread = None

    def pathfinding(self, scene):
        self._lock.acquire()

        car = self._car
        next_path = self._next_path
        current_path = self._path
        
        self._lock.release()
        
        actions = find_path(scene, car, next_path, current_path)
        
        self._lock.acquire()
        
        self._actions = actions
        self._action_changed = True

        self._lock.release()
