from helpers.dotenv import dotenv, get_env
from engine.scene.frame import Frame

if __name__ == "__main__":
    dotenv()

    frame = Frame()

    # json_world = json.loads(open("world/assets/world.json", mode='r').read())
    # world = World.load(json_world)

    scene = frame.get_scene()

    # modelA = models.add(f'{get_env("MODELS_DIR")}/cliff/cliff')
    # road = RoadModel([10, 10], [100, 100], models)

    frame.show()
