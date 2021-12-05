class MTLLoader:

    def __init__(self, content: list):
        self._content = [line.split() for line in content if len(line) > 1]
        self._get_materials()

    @staticmethod
    def load(relative_path: str):
        relative_path = relative_path.split('.')[0] + ".mtl"
        return MTLLoader(open(relative_path, 'r', encoding="utf-8").readlines())

    def _get_materials(self) -> dict:
        result, content = {}, self._content
        i, j = 0, 0
        while i < len(content):
            if content[i][0] == 'newmtl' and content[i][1] not in result:
                result[content[i][1]] = {}
                j = i + 1
                while j < len(content) and content[j][0] != 'newmtl':
                    result[content[i][1]][content[j][0]] = content[j][1]
                    j += 1
            i += 1
        return result

    def _get_material(self, metadata: list):
        pass


"""
"Ka" nous donne la couleur ambiante (la couleur de l'objet sans lumière directe), RVB entre 0 (Min) et 1 (Max)
"Kd" est utilisé pour la couleur diffuse (la couleur de l'objet sous lumière blanche)
"Ks" pour la couleur spéculaire (specular)
"Ke" pour la couleur émissive (emissive)
"Ni" pour la densité optique
"Ns" pour le specular exponent entre 0 et 100
"d" pour la transparence entre 0 et 1 (aucune transparence)
"illum" pour les paramètres de lumières
"map_kd" (ks, ka) pour la texture utilisé diffuse (specular, ambiante)
"""
