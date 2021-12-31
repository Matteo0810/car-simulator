from helpers.dotenv import get_env
from world.road import Path
from helpers.utils import property_get


class LightsType:
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


class Intersection:
    def __init__(self, inbounds, outbounds, ligths_type):
        """
            inbounds est une liste de PathInfo
            outbounds est une liste de Path
        """
        self._inbounds = inbounds
        self._outbounds = outbounds
        self._ligths_type = ligths_type
        
        self._lights_group_count = max((info.lights_group for info in inbounds))
        
        self._green_group = 0
        self._lights_time = get_env("TRAFFIC_LIGHTS_DELAY")
    
    def tick(self, world, dt):
        self._lights_time -= dt
        if self._lights_time < 0:
            self._lights_time = get_env("TRAFFIC_LIGHTS_DELAY")
            self._green_group = (self._green_group + 1) % self._lights_group_count
    
    @property
    def inbounds(self):
        return self._inbounds
    
    @property
    def outbounds(self):
        return self._outbounds
    
    @property
    def ligths_type(self):
        return self._ligths_type
