from tkinter import *
from engine.objloader import ObjLoader
from helpers.dotenv import dotenv, get_env

dotenv()

root = Tk()
root.resizable(False, False)

canvas = Canvas(
    master=root,
    height=get_env('HEIGHT'),
    width=get_env('WIDTH'),
    bg="black"
)

obj = ObjLoader.load("./assets/test.obj")
obj.render(canvas)
canvas.pack()

root.mainloop()
