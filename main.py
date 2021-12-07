from tkinter import Tk
from engine.scene.scene import Scene
from world.car import Car, CarModel
from pygame import Vector2
from helpers.dotenv import dotenv


def rotate_animation(animation):
    for i in range(50):
        animation.add_frame(lambda polygon: polygon.rotate('x', i))
    return animation


if __name__ == "__main__":
    dotenv()

    root = Tk()
    root.title('Car simulator')
    root.resizable(False, False)

    scene = Scene(root)
    car = Car(scene, Vector2(0, 0), 0, CarModel("default", (10, 20), 1, (0, 255, 0)))
    model = scene.get_models().add('world/assets/cube/cube.obj', car.get_center_of_mass())
    scene.show()

    """
    model.get_animations()\
        .add('test', lambda animation: rotate_animation(animation))\
        .play(scene)
    """
    
    dt = (time() - last_frame)*2
    scene.get_controller().tick(dt)
    scene.update(dt)
    
    last_frame = time()
    sleep(0.01)

    root.mainloop()
