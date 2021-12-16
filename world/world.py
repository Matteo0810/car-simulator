import json

class World:
    def __init__(self, cars):
        self._cars = cars
    
    
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
    
    
    
        
