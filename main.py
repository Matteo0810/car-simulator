from tkinter import Tk
from engine.scene.scene import Scene
from helpers.dotenv import dotenv


if __name__ == "__main__":
    dotenv()

    root = Tk()
    root.title('Car simulator')
    root.resizable(False, False)
    scene = Scene(root)

    scene.get_models().add('assets/cube.obj')
    scene.show()

    root.mainloop()
