import json
from pygame import Vector2
from engine.model.objloader import ObjLoader
from helpers.dotenv import get_env


class Model:
    def __init__(self, polygon, hitbox):
        self._polygon = polygon
        self._hitbox = hitbox
    
    @property
    def polygon(self):
        return self._polygon
    
    @property
    def hitbox(self):
        return self._hitbox
    
    @staticmethod
    def load(name):
        hitbox = [Vector2(**p) for p in json.loads(get_env("MODELS_DIR") + name + "/hitbox.json")]
        polygon = ObjLoader.load(get_env("MODELS_DIR") + name + "/" + name).get_polygon()
        return Model(polygon, hitbox)
