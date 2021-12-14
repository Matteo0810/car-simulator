from tkinter import Tk
from engine.scene.scene import Scene
from helpers.dotenv import dotenv


def rotate_animation(animation):
    for i in range(30):
        animation.add_frame(lambda polygon: polygon.rotate('y', i))
    return animation


if __name__ == "__main__":
    dotenv()

    root = Tk()
    root.title('Car simulator')
    root.resizable(False, False)

    scene = Scene(root)
    model = scene.get_models().add('world/assets/cube/cube.obj')
    scene.show()
 
    """
    model.get_animations()\
        .add('rotation', lambda animation: rotate_animation(animation))\
        .play(scene)
    """

    root.mainloop()
