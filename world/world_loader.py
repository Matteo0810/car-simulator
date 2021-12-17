import json

def load(chem):
    content = open(chem, mode='r').read()
    print(json.loads(content))
    content = json.loads(content)
    return World(content)
        
world = load('assets/world.json')
print(world)






        
        
        
        
        
        
        


    