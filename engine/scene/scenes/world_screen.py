from math import cos, sin, pi
from time import time, sleep
from threading import Thread, main_thread

from engine.scene.scene import Scene

from engine.ai.car_ai import AIImpl

from helpers.physics import check_collision
from helpers.build_ground import build_ground
from helpers.dotenv import get_env
from helpers.vector import Vector3, Vector2

from world.car import Car, CarType
from world.world import World

ROAD_MODEL_LENGTH = 8 * 1.75 - 0.1
ROAD_MODEL_WIDTH = 8

CAR_MODELS = ["low_car_red", "low_car_blue"] * 3


class WorldScreen(Scene):
    world = None

    def __init__(self, root):
        super().__init__(root)

        self.events.on('leave', self._stop)
        self.add_button((20, 20), "Quitter", lambda: self.gui.use(self.gui.screens['title']))
        self._render()

    def _render(self):
        build_ground(self.get_models(), self.get_camera())

        self.get_camera() \
            .set_direction(0, -90) \
            .move(0, 0, 100) \
            .set_zoom(0.8)

        self._user_car = None
        self._is_user_driving = False
        self._landscape = None
        self._stop_thread = False

        Thread(target=self._thread).start()

        self.after(100, self.update_loop)
        
        pos_mul = 1.
        pos_offset = Vector2(0, 0)

        self._render_cars()
        self._build_intersections(pos_mul, pos_offset)
        self._build_road(pos_mul, pos_offset)

    def _render_cars(self):
        for i in range(1):
            path = self.world.roads[i].paths[0]
            car = Car(self.world, path.start + path.direction * 10, path.direction.angle(),
                      CarType(CAR_MODELS[i-1], 2.2, 5, 1, (0, 255, 0), 10))
            car.ai = AIImpl(path, car)
            self.world.cars.append(car)
            car.ai.start_thread(None)

    def _build_road(self, pos_mul, pos_offset):
        for road in self.world.roads:
            A, B = road.start, road.end
            AB: Vector2 = (B - A)
            A, B = A + AB.normalize() * get_env("ROAD_WIDTH") / 2, road.end - AB.normalize() * get_env("ROAD_WIDTH") / 2
            AB: Vector2 = (B - A)

            rotation = AB.angle() / pi * 180 + 90

            for i in range(int(AB.length() // ROAD_MODEL_LENGTH)):
                mid_road = A + (i + 0.5) * AB.normalize() * ROAD_MODEL_LENGTH
                mid_road *= pos_mul
                mid_road += pos_offset
                self.get_models().add('roads/road', size=1.75,
                                      position=Vector3.from_vector2(mid_road, 0.1)).rotate('z', rotation)

            mid_road_last = B - AB.normalize() * ROAD_MODEL_LENGTH / 2
            mid_road_last *= pos_mul
            mid_road_last += pos_offset
            self.get_models().add('roads/road', size=1.75, position=Vector3.from_vector2(mid_road_last, 0.1)) \
                .rotate('z', rotation)

    def _build_intersections(self, pos_mul, pos_offset):
        for intersection in self.intersections:
            middle = (sum(inbound.path.end for inbound in intersection.inbounds) + sum(
                outbound.start for outbound in intersection.outbounds)) \
                     / len(intersection.inbounds) / 2
            middle *= pos_mul
            middle += pos_offset
            self.get_models().add('roads/intersections/intersection', size=1.3,
                                  position=Vector3.from_vector2(middle, 0.099))

    def _tick(self, dt):
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
        last_frame = time()
        while main_thread().is_alive() and not self._stop_thread:
            frame_start = time()
            dt = (frame_start - last_frame)
            self._tick(dt * 1)
            last_frame = frame_start
            
            sleep(max(0., 0.01 - (time() - frame_start)))
        
        for car in self.world.cars:
            if isinstance(car.ai, AIImpl):
                car.ai.stop_thread()

    def update(self):
        self.clear()
        faces = []

        if not self._landscape:
            self._landscape = []
            for polygon in self.get_models().all():
                faces.extend(polygon.faces)

            for face in sorted(faces, key=lambda f: f.avg_dist()):
                self._landscape.append(face.create(self))
        else:
            for shape in self._landscape:
                shape.draw(self)

        faces = []

        for car in self.world.cars:
            car.model.polygon.set_camera(self.get_camera())
            car.model.polygon.set_position(*Vector3.from_vector2(car.position, 1))
            car.model.polygon.set_rotation('z', car.angle / pi * 180 + 90)
            faces.extend(car.model.polygon.faces)

        for face in sorted(faces, key=lambda f: f.avg_dist()):
            face.create(self)

        if self.is_dev:
            self._fps.update()
    
    def update_loop(self):
        if self._stop_thread:
            return
        
        max_car_distance = 40
        
        if len(self.world.cars) > 0 and not self._user_car:
            self._user_car = self.world.cars[0]
        
        if self._user_car:
            if self._user_car.position.distance(self.get_camera().position.xy) > max_car_distance:
                self._landscape = None
                camera = self.get_camera()
                car = self._user_car
                camera_tp = car.ai.next_path.start if isinstance(car.ai, AIImpl) else car.position
                camera_pos = min(max_car_distance-1, camera_tp.distance(car.position)) * (camera_tp - car.position).normalize() + car.position
                camera.set_position(*Vector3.from_vector2(camera_pos, camera.position.z))
        
        self.update()
        
        self.after(1, self.update_loop)

    def _stop(self):
        self._stop_thread = False

    @property
    def intersections(self):
        return list(
            set([road.paths[0].intersection for road in self.world.roads] + [road.paths[1].intersection for road in
                                                                             self.world.roads]))

    @staticmethod
    def with_(world):
        return type("WorldScreen_Impl", (WorldScreen,), {"world": world})
