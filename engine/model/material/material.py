from helpers.color import Color


class Material:

    def __init__(self, metadata):
        self._metadata = metadata

    def get_alpha(self):
        return self._metadata['d']

    def get_ambient_color(self):
        return Color.from_list(self._metadata['Ka']+[self.get_alpha()])

    def get_diffuse_color(self):
        return Color.from_list(self._metadata['Kd']+[self.get_alpha()])

    def get_specular_color(self):
        return Color.from_list(self._metadata['Ks'] + [self.get_alpha()])

    def get_emissive_color(self):
        return Color.from_list(self._metadata['Ke'] + [self.get_alpha()])

    def get_specular_exponent(self):
        return self._metadata['Ns']

    def get_optical_density(self):
        return self._metadata['Ni']

    def get_illuminations(self):
        return self._metadata['illum']

    def get_color(self):
        if 'color' not in self._metadata:
            return Color.from_list([255, 255, 255, 1])
        return Color.from_list(self._metadata['color'] + [1])
