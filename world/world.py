from helpers.vector import Vector2
from world.road import Road


class World:
    def __init__(self, cars):  # TODO : ajouter les paramètres manquants
        """
            Prend en paramètre les éléments du monde, comme les voitures, les routes et les obstacles
        """
        self._cars = cars
        #self._roads ...

    @property
    def cars(self):
        return self._cars

    @staticmethod
    def load(content):
        """
        :param content: dictionnaire représentant le json du monde
        :return: le monde
        """

        cars = []
        
        """
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
            
            # puis on créé l'objet
            # road = Road(start, ...)
            pass
        
        # il faudra ajouter des paramètres au constructeur et les renseigner ici
        return World(cars)
