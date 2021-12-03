from tkinter import Tk
from engine.scene.scene import Scene
from helpers.dotenv import dotenv

dotenv()

root = Tk()
root.resizable(False, False)
scene = Scene(root)

scene.add_model('./assets/test.obj')
scene.show()

root.mainloop()
