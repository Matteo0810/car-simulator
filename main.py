from tkinter import *
from engine.objloader import ObjLoader

WIDTH, HEIGHT = 1500, 1000

root = Tk()
root.resizable(False, False)

canvas = Canvas(master=root, height=HEIGHT, width=WIDTH, bg="black")
obj = ObjLoader.load("./assets/pumpkin.obj", (1000, 1000), 6, 200)
obj.render(canvas)
canvas.pack()
root.mainloop()
