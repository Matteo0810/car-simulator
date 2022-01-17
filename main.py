from helpers.dotenv import dotenv
from engine.scene.frame import Frame

if __name__ == "__main__":
    dotenv()

    frame = Frame()
    frame.show()
