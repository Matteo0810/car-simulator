from helpers.color import Color


class Material:

    def __init__(self, metadata):
        self._metadata = metadata

    def get_alpha(self):
        return self._metadata['d']

    def get_ambient_color(self):
        return Color.from_list(self._metadata['Ka']+[self.get_alpha()])

    def get_diffuse_color(self):
        return self._metadata['Kd']

    def get_specular_color(self):
        return self._metadata['Ks']

    def get_emissive_color(self):
        return self._metadata['Ke']

    def get_specular_exponent(self):
        return self._metadata['Ns']

    def get_optical_density(self):
        return self._metadata['Ni']

    def get_illuminations(self):
        return self._metadata['illum']
