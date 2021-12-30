import json
from enum import Enum

from pygame import Vector2
from engine.model.objloader import ObjLoader
from helpers.dotenv import get_env


class Behaviour(Enum):
    VOID = 0
    COLLIDEABLE = 1


class Model:
    def __init__(self, polygon, hitbox, behaviour):
        self._polygon = polygon
        self._hitbox = hitbox
        self._behaviour = behaviour
    
    @property
    def polygon(self):
        return self._polygon
    
    @property
    def hitbox(self):
        return self._hitbox
    
    @property
    def behaviour(self):
        return self._behaviour
    
    @staticmethod
    def load(name):
        j_hitbox = json.loads(get_env("MODELS_DIR") + name + "/hitbox.json.json")
        behaviour = Behaviour[j_hitbox["type"]]
        hitbox = [Vector2(**p) for p in j_hitbox["points"]]
        polygon = ObjLoader.load(get_env("MODELS_DIR") + name + "/" + name).get_polygon()
        return Model(polygon, hitbox, behaviour)
