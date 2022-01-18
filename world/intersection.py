from enum import Enum
from math import pi

from helpers.dotenv import get_env
from helpers.vector import Vector2
from world.road import Path
from helpers.utils import property_get


class LightsType(Enum):
    # NONE: les voitures ne respectent que la priorité a droite
    NONE = 0
    
    # STOPS: si une voiture est face a un stop et qu'une voiture arrive d'une voie sans stop, elle attend que celle-ci
    # passe. Les voitures qui n'ont pas de stop passent directement
    STOPS = 1
    
    # LIGHTS: les voies sont séparées en groupe de feu tricolores. Une voiture arrivant a une voie doit attendre que le
    # feu de sa voie soit vert pour passer. Les feux alternes par groupe.
    LIGHTS = 2


class PathInfo:
    def __init__(self, path: Path, has_stop=False, lights_group=-1):
        self._path = path
        self._has_stop = has_stop
        self._lights_group = lights_group
    
    path = property_get("path")
    has_stop = property_get("has_stop")
    lights_group = property_get("lights_group")
    
    def get_inbound_cars(self, world):
        cars = []
        for car in world.cars:
            if self._path.distance(car.position) < 3\
                    and abs(Vector2.of_angle(car.angle + pi).angle(self.path.direction)) < 1\
                    and car.position.distance(self._path.end) < 30:
                cars.append(car)
        return cars


class Intersection:
    def __init__(self, inbounds, outbounds, ligths_type, id_):
        """
            inbounds est une liste de PathInfo
            outbounds est une liste de Path
        """
        if ligths_type is None or type(ligths_type) is not LightsType:
            raise TypeError(f"ligths_type must be of type LightsType, not {type(ligths_type)}")
        
        self._inbounds = inbounds
        self._outbounds = outbounds
        self._ligths_type = ligths_type
        
        self._lights_group_count = max((info.lights_group for info in inbounds))
        
        self._green_group = 0
        self._lights_time = get_env("TRAFFIC_LIGHTS_DELAY")
        self._mid = sum((in_.path.end - in_.path.direction * get_env("ROAD_WIDTH") / 2 for in_ in self.inbounds)) / len(self.inbounds)

        self._id = id_
    
    def tick(self, world, dt):
        if self.ligths_type == LightsType.LIGHTS:
            self._lights_time -= dt
            if self._lights_time < 0:
                self._lights_time = get_env("TRAFFIC_LIGHTS_DELAY")
                self._green_group = (self._green_group + 1) % (self._lights_group_count + 1)
            
    def is_green(self, path):
        for inbound in self._inbounds:
            if inbound.path == path:
                return inbound.lights_group == self._green_group
        raise ValueError("arg is not an inbound")

    @property
    def priority_ordered_inbounds(self):
        if self.ligths_type == LightsType.NONE:
            return [self._inbounds]
        if self.ligths_type == LightsType.STOPS:
            return [[in_ for in_ in self._inbounds if not in_.has_stop], [in_ for in_ in self._inbounds if in_.has_stop]]
        if self.ligths_type == LightsType.LIGHTS:
            return [[in_ for in_ in self._inbounds if in_.lights_group == self._green_group],
                    [in_ for in_ in self._inbounds if in_.lights_group != self._green_group]]
        raise AssertionError()

    def has_priority(self, inbound, desired_outbound, world):
        if len(self.inbounds) <= 2:
            return True
        for i in range(len(self.priority_ordered_inbounds)):
            if any(in_.path == inbound for in_ in self.priority_ordered_inbounds[i]):
                angle_v = inbound.end - self._mid
                
                others = [an_inbound.path for an_inbound in self.priority_ordered_inbounds[i] if len(an_inbound.get_inbound_cars(world)) > 0 and an_inbound.path != inbound]
                
                priority = True
                
                for other in others:
                    angle = (inbound.end - self._mid).angle(other.end - self._mid)
                    if 0 < angle < pi - 0.01:
                        pass
                    elif 0 > angle > -pi + 0.01:
                        priority = False
                    elif (desired_outbound.end - self._mid).angle(other.end - self._mid) < 0:
                        priority = False
                return priority
            else:
                if self.ligths_type == LightsType.LIGHTS:
                    return False
                for an_inbound in self.priority_ordered_inbounds[i]:
                    if len(an_inbound.get_inbound_cars(world)) > 0:
                        return False
        
        print("C'est pas normal ca (intersection.py : Intersection#has_priority)")
        # priority_ordered_inbounds() ne contient pas inbound
        return True
    
    @property
    def inbounds(self):
        return self._inbounds
    
    @property
    def outbounds(self):
        return self._outbounds
    
    @property
    def ligths_type(self):
        return self._ligths_type
    
    @property
    def id(self):
        return self._id


class IntersectionBuilder:
    def __init__(self, ligths_type, id_):
        self._inbounds = []
        self._outbounds = []
        self._ligths_type = ligths_type
        self._built = None
        self._id = id_
    
    def add_road(self, road, is_start, has_stop=False, lights_group=-1):
        self._inbounds.append(PathInfo(road.paths[is_start], has_stop, lights_group))
        self._outbounds.append(road.paths[not is_start])
        return self
    
    def build(self):
        self._built = Intersection(self._inbounds, self._outbounds, self._ligths_type, self._id)
        return self._built
    
    @property
    def ligths_type(self):
        return self._ligths_type
    
    @property
    def built(self):
        return self._built
