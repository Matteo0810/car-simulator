from tkinter import *
from engine.objloader import ObjLoader
import time

WIDTH, HEIGHT = 1500, 1000

root = Tk()
root.resizable(False, False)

canvas = Canvas(master=root, height=HEIGHT, width=WIDTH, bg="black")

obj = ObjLoader.load("./assets/test.obj", (1500, 1000), 6, 100)
obj.render(canvas)
canvas.pack()

root.mainloop()
