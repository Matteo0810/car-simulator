from enum import Enum


class Material:

    def __init__(self, metadata):
        self._metadata = metadata
        print(self._metadata)

    def get_illuminations(self):
        return Illuminations[int(self._metadata['illum'])]


class Illuminations(Enum):
    pass


"""
"Ka" nous donne la couleur ambiante (la couleur de l'objet sans lumière directe),
 RVB entre 0 (Min) et 1 (Max)
"Kd" est utilisé pour la couleur diffuse (la couleur de l'objet sous lumière blanche)
"Ks" pour la couleur spéculaire (specular)
"Ke" pour la couleur émissive (emissive)
"Ni" pour la densité optique
"Ns" pour le specular exponent entre 0 et 100
"d" pour la transparence entre 0 et 1 (aucune transparence)
"illum" pour les paramètres de lumières
"map_kd" (ks, ka) pour la texture utilisé diffuse (specular, ambiante)
"""
