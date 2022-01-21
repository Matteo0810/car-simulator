import json

from engine.model.objloader import ObjLoader
from helpers.dotenv import get_env
from helpers.vector import Vector2


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
        j_hitbox = json.loads(get_env("ASSETS_DIR_DIR") + "models/" + name + "/hitbox.json.json")
        hitbox = [Vector2(**p) for p in j_hitbox["points"]]
        polygon = ObjLoader.load(get_env("ASSETS_DIR") + "models/" + name + "/" + name).get_polygon()
        return Model(polygon, hitbox)
