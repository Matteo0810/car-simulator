from enum import Enum

from helpers.vector import Vector2
from world.road import Road


class GroundType(Enum):
    GRASS = 0
    ROAD = 1
    VOID = 2

    @property
    def friction_loss(self):
        return [15, 8, 100000][self.value]
    
    @property
    def grip(self):
        return [20, 30, 0][self.value]


class World:
    def __init__(self, cars, roads, obstacles):
        """
            Prend en paramètre les éléments du monde, comme les voitures, les routes et les obstacles
        """
        self._cars = cars
        self._roads = roads
        self._obstacles = obstacles

    @property
    def cars(self):
        return self._cars
    
    @property
    def roads(self):
        return self._roads

    @property
    def obstacles(self):
        return self._obstacles
    
    def get_ground_at(self, position):
        return GroundType(any((road.contains(position) for road in self._roads)))

    @staticmethod
    def load(content):
        """
        :param content: dictionnaire représentant le json du monde
        :return: le monde
        """
        roads = []
        cars = []
        intersection = []
        obstacles = []

        """""
            attention, content["roads"] est une liste qui contient d'autres dictionnaires, qui ressemblent à ca:
            {
                "start": [x, y],
                etc...
            }
            la liste roads définie ici devra par contre contenir des objets Road
        """
        roads = []

        for j_road in content["roads"]:
            # j_road pour indiquer que c'est un dictionnaire issu d'un fichier json

            # on récupère les attributs et on les tranforme un par un
            start = Vector2(*j_road["start"])
            end = Vector2(*j_road["end"])
            speed_limit = j_road["speed_limit"]


            # puis on créé l'objet
            road = Road(start, end, speed_limit, None, None)
            roads.append(road)

        # il faudra ajouter des paramètres au constructeur et les renseigner ici
        return World(cars, roads, obstacles)
