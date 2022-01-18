from enum import Enum
import json

from helpers.vector import Vector2
from world.road import Road
from world.intersection import IntersectionBuilder, LightsType


class GroundType(Enum):
    GRASS = 0
    ROAD = 1
    VOID = 2

    @property
    def friction_loss(self):
        return [3, 1, 0][self.value]
    
    @property
    def grip(self):
        return [0.7, 0.9, 0][self.value]


class World:
    def __init__(self, props, roads, obstacles):
        """
            Prend en paramètre les éléments du monde, comme les voitures, les routes et les obstacles
        """
        self._props = props
        self._cars = []
        self._roads = roads
        self._obstacles = obstacles

    @property
    def props(self):
        return self._props

    @property
    def cars(self):
        return self._cars
    
    @property
    def roads(self):
        return self._roads

    @property
    def obstacles(self):
        return self._obstacles

    @property
    def collideables(self):
        return self._obstacles + self._cars
    
    def get_ground_at(self, position):
        return GroundType(any((road.contains(position) for road in self._roads)))
    
    @staticmethod
    def _get_intersections(loaded_intersections, j_content, si_id, ei_id):
        if si_id == -1:
            start_intersection = IntersectionBuilder(LightsType.NONE, si_id)
        else:
            if si_id in loaded_intersections:
                start_intersection = loaded_intersections[si_id]
            else:
                start_intersection = IntersectionBuilder(LightsType[j_content["intersections"][si_id]["type"]], si_id)
    
        if ei_id == -1:
            end_intersection = IntersectionBuilder(LightsType.NONE, ei_id)
        else:
            if ei_id in loaded_intersections:
                end_intersection = loaded_intersections[ei_id]
            else:
                end_intersection = IntersectionBuilder(LightsType[j_content["intersections"][ei_id]["type"]], ei_id)

        loaded_intersections[si_id] = start_intersection
        loaded_intersections[ei_id] = end_intersection
        return start_intersection, end_intersection
    
    @staticmethod
    def _add_road(j_intersection, intersection, road_id, road, is_start):
        if intersection.ligths_type == LightsType.NONE:
            intersection.add_road(road, is_start)
    
        elif intersection.ligths_type == LightsType.STOPS:
            intersection.add_road(road, is_start, has_stop=(road_id in j_intersection["stops"]))
    
        elif intersection.ligths_type == LightsType.LIGHTS:
            group_id = -1
            for i in range(len(j_intersection["groups"])):
                if road_id in j_intersection["groups"][i]:
                    group_id = i
            if group_id == -1:
                raise IndexError(f"Le groupe de feu n'est pas renseigné pour la route {road_id}")
            intersection.add_road(road, is_start, lights_group=group_id)
            
    @staticmethod
    def load(content):
        """
        :param content: dictionnaire représentant le json du monde
        :return: le monde
        """
        content = json.loads(content) if type(content) is str else content
        roads = []
        obstacles = []
        
        # On range les intersections par id
        # Quand on charge une route et que l'intersection n'est pas chargée, on la charge et on l'ajoute au dictionnaire
        # Quand l'intersection est déjà chargée, on la récupère simplement
        intersections = {}

        """""
            attention, content["roads"] est une liste qui contient d'autres dictionnaires, qui ressemblent à ca:
            {
                "start": [x, y],
                etc...
            }
            la liste roads définie ici devra par contre contenir des objets Road
        """
        
        for road_id in range(len(content["roads"])):
            j_road = content["roads"][road_id]
            # j_road pour indiquer que c'est un dictionnaire issu d'un fichier json
            
            # on récupère les attributs et on les tranforme un par un
            start = Vector2(*j_road["start"])
            end = Vector2(*j_road["end"])
            speed_limit = j_road["speed_limit"]
            
            si_id = j_road["start_intersection"]
            ei_id = j_road["end_intersection"]

            start_intersection, end_intersection = World._get_intersections(intersections, content, si_id, ei_id)
            
            # puis on créé l'objet
            road = Road(start, end, speed_limit, start_intersection, end_intersection, road_id)
            roads.append(road)
            
            World._add_road(content["intersections"][si_id], start_intersection, road_id, road, True)
            World._add_road(content["intersections"][ei_id], end_intersection, road_id, road, False)
        
        for road in roads:
            road.intersection_built()
        
        return World(content['props'], roads, obstacles)
