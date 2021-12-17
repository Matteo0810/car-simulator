import json


class World:
    def __init__(self, content):
        """
            content: dictionnaire contenant des voitures,des routes, des d'intersections et des obstacles

            notre but ici va être de trier tout ce contenu dans plusieurs liste: exemple: une liste de voitures,
            une liste de route, une liste d'intersection et une liste d'obstacles un exemple si dessus d'un attributs
            _cars (un _ au début pour dire que cette attribut est privé et donc accéssible que dans cette classe) on
            le définit comme une liste vide pour ensuite le remplir avec les voitures que l'ont trouvera dans le
            contenu
        """
        self._cars = []

    @property
    def cars(self):
        return self._cars

    @staticmethod
    def load(chem):
        content = open(chem, mode='r').read()
        print(json.loads(content))
        content = json.loads(content)

        return World(content)


World.load("assets/world.json")
