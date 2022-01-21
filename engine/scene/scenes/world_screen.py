import json
from time import time, sleep
from threading import Thread

from engine.physics import check_collision
from engine.scene.scene import Scene
from engine.car_controller import CarController
from helpers.dotenv import get_env
from world.world import World


class WorldScreen(Scene):
    world = None
    
    def __init__(self, root):
        super().__init__(root, True)
        self._config = json.loads(open('world/assets/worlds_config.json', mode='r').read())

        self._default_camera.move(*self._config['camera']['position'])
        self._last_frame = time()
        self.add_controller(CarController(self))
        # car = Car(self.world, Vector2(0, 0), 0, CarType("default", 2.2, 5, 1, (0, 255, 0), 15))
        # car.ai = CarController ? une classe qui extends de AI (voir PygameController)
        # self.world.cars.append(car)

        # rendering
        x, y, z = self._config['camera']['direction']
        self.get_models().add(f'grounds/ground_{self.world.props["type"]}/ground', size=15)\
            .rotate('x', x).rotate('y', y).rotate('z', z)
        self._render()

        self.bind('<Key>', self._reload)
        Thread(target=self._thread).start()

    def _render(self):
        x, y, z = self._config['camera']['direction']
        for road in self.world.roads:
            (xA, yA), (xB, yB) = road.start, road.end
            # TODO problem with road position
            self.get_models().add('roads/road', position=((xA + xB) // 2, (yA + yB) // 2), size=10, distance=5)\
                .rotate('x', x).rotate('y', y).rotate('z', z)

    def _update(self, dt):
        for intersection in self.intersections:
            intersection.tick(self.world, dt)

        for car in self.world.cars:
            car.ai.pre_tick(dt)
        for car in self.world.cars:
            car.tick(dt)
        for car1 in self.world.cars:
            for car2 in self.world.cars:
                if car1 is not car2:
                    check_collision(car1, car2, dt)
        for car in self.world.cars:
            car.update_last_position(dt)
            car.reconstruct()

    def _thread(self):
        while True:
            frame_start = time()
            dt = (frame_start - self._last_frame)
            self._update(dt * 0.8)
            self._last_frame = frame_start

            sleep(max(0., 0.001 - (time() - frame_start)))

    def _reload(self, event):
        if event.char == 'r':
            self.gui.use(WorldScreen.with_(World.load(open(f'{get_env("ASSETS_DIR")}worlds/{self.world.props["file_name"]}.json'
                                                           , mode='r', encoding='utf-8').read())))

    @property
    def intersections(self):
        return list(
            set([road.paths[0].intersection for road in self.world.roads] + [road.paths[1].intersection for road in
                                                                             self.world.roads]))

    @staticmethod
    def with_(world):
        return type("WorldScreen_Impl", (WorldScreen,), {"world": world})
