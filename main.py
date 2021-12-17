from tkinter import Tk
from engine.scene.scene import Scene
from helpers.dotenv import dotenv


def rotate_animation(animation):
    for i in range(30):
        animation.add_frame(lambda polygon: polygon.rotate('x', i))
    return animation


if __name__ == "__main__":
    dotenv()

    root = Tk()
    root.title('Car simulator')
    root.resizable(False, False)

    scene = Scene(root)
    models = scene.get_models()

    modelA = models.add(f'{models.resources}/cube/cube')
    # modelB = models.add(f'{models.resources}/cube/cube.obj')
    scene.show()

    """
    model.get_animations()\
        .add('rotation', lambda animation: rotate_animation(animation))\
        .play(scene)
    """

    root.mainloop()
