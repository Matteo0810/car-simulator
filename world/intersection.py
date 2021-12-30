class LightsType:
    # NONE: les voitures ne respectent que la priorité a droite
    NONE = 0
    
    # STOPS: si une voiture est face a un stop et qu'une voiture arrive d'une voie sans stop, elle attend que celle-ci
    # passe. Les voitures qui n'ont pas de stop passent directement
    STOPS = 1
    
    # LIGHTS: les voies sont séparées en groupe de feu tricolores. Une voiture arrivant a une voie doit attendre que le
    # feu de sa voie soit vert pour passer. Les feux alternes par groupe.
    LIGHTS = 2


class Intersection:
    def __init__(self, inbounds, outbounds, ligths_type):
        self._inbounds = inbounds
        self._outbounds = outbounds
        self._ligths_type = ligths_type
    
    @property
    def inbounds(self):
        return self._inbounds
    
    @property
    def outbounds(self):
        return self._outbounds
    
    @property
    def ligths_type(self):
        return self._ligths_type
