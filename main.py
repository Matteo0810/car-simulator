from tkinter import Tk
from engine.scene.scene import Scene
from helpers.dotenv import dotenv, get_env
import json
from world.world import World


def rotate_animation(animation):
    for i in range(30):
        animation.add_frame(lambda polygon: polygon.rotate('x', i))
    return animation


if __name__ == "__main__":
    dotenv()

    root = Tk()
    root.title('Car simulator')
    root.resizable(False, False)

    # json_world = json.loads(open("world/assets/world.json", mode='r').read())
    # world = World.load(json_world)
    
    scene = Scene(root)
    models = scene.get_models()

    modelA = models.add(get_env("MODELS_DIR") + "cliff/cliff")
    scene.show()

    """
    model.get_animations()\
        .add('rotation', lambda animation: rotate_animation(animation))\
        .play(scene)
    """

    root.mainloop()
