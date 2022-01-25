import json
import random
from math import cos, sin, pi
from time import time, sleep
from threading import Thread, main_thread

from engine.scene.scene import Scene
from engine.ai.car_ai import AIImpl
from engine.model.material.material import Material
from engine.model.polygon.face import Face
from engine.model.polygon.polygon import Polygon
from engine.model.polygon.vertex import Vertex
from helpers.physics import check_collision
from helpers import improved_noise
from helpers.dotenv import get_env
from helpers.vector import Vector3, Vector2
from world.car import Car, CarType
from world.world import World

ROAD_MODEL_LENGTH = 8 * 1.75 - 0.1
ROAD_MODEL_WIDTH = 8
INTERSECTION_MODEL_WIDTH = 8


class WorldScreen(Scene):
    world = None

    def __init__(self, root):
        super().__init__(root)
        self._config = json.loads(open(f'{get_env("ASSETS_DIR")}/worlds_config.json', mode='r').read())

        # self._car_controller = CarController()
        
        for i in range(1, 3):
            car = Car(self.world, Vector2(-10, 30 * i), 0, CarType("car", 2.2, 5, 1, (0, 255, 0), 10))
            car.ai = AIImpl(self.world.roads[0].paths[0], car)
            self.world.cars.append(car)
            # ne marche pas si ca tourne plusieurs fois
            car.ai.start_thread(None)

        self.add_button((20, 20), "Quitter", lambda: self.gui.use(self.gui.scenes['title_screen']))

        # rendering
        camera = self.get_camera()
        camera.set_direction(*self._config['camera']['direction'])
        camera.move(*self._config['camera']['position'])
        camera.set_zoom(0.6)
        
        self._user_car = None
        self._is_user_driving = False
        
        self._landscape = None
        
        self._render()
        self.bind('<Key>', self._handle_keys)
        self._stop_thread = False
        Thread(target=self._thread).start()
        self.after(100, self.update_loop)

    def _render(self):
        self.build_ground()
        
        pos_mul = 1.
        pos_offset = Vector2(0, 0)
        
        for intersection in self.intersections:
            middle = (sum(inbound.path.end for inbound in intersection.inbounds) + sum(outbound.start for outbound in intersection.outbounds))\
                     / len(intersection.inbounds) / 2
            middle *= pos_mul
            middle += pos_offset
            self.get_models().add('roads/intersections/intersection', size=1.3, position=Vector3.from_vector2(middle, 0.099))

        for road in self.world.roads:
            A, B = road.start, road.end
            AB: Vector2 = (B - A)
            A, B = A + AB.normalize() * get_env("ROAD_WIDTH")/4, road.end - AB.normalize() * get_env("ROAD_WIDTH")/4
            AB: Vector2 = (B - A)

            rotation = AB.angle() / pi * 180 + 90

            for i in range(int(AB.length() // ROAD_MODEL_LENGTH)):
                mid_road = A + (i + 0.5) * AB.normalize() * ROAD_MODEL_LENGTH
                mid_road *= pos_mul
                mid_road += pos_offset
                self.get_models().add('roads/road', size=1.75, position=Vector3.from_vector2(mid_road, 0.1)).rotate('z', rotation)

            mid_road_last = B - AB.normalize() * ROAD_MODEL_LENGTH / 2
            mid_road_last *= pos_mul
            mid_road_last += pos_offset
            self.get_models().add('roads/road', size=1.75, position=Vector3.from_vector2(mid_road_last, 0.1))\
                .rotate('z', rotation)
    
    def update(self, callback=None):
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
            #print(car.position)
            car.update_last_position(dt)
            car.reconstruct()

    def _thread(self):
        last_frame = time()
        while main_thread().is_alive() and not self._stop_thread:
            frame_start = time()
            dt = (frame_start - last_frame)
            self._tick(dt * 0.5)
            last_frame = frame_start
            
            sleep(max(0., 0.01 - (time() - frame_start)))
        
        for car in self.world.cars:
            if isinstance(car.ai, AIImpl):
                car.ai.stop_thread()
    
    def update_loop(self):
        if self._stop_thread:
            return
        
        if len(self.world.cars) > 0 and not self._user_car:
            self._user_car = self.world.cars[0]
        
        if self._user_car:
            if self._user_car.position.distance(self.get_camera().position.xy) > 40:
                self._landscape = None
                camera = self.get_camera()
                camera.set_position(*Vector3.from_vector2(self._user_car.position, camera.position.z))
        
        self.update()
        
        self.after(1, self.update_loop)

    def _handle_keys(self, event):
        if event.char == 'd':
            self.get_camera().move(cos(self.get_camera().yaw * pi / 180), sin(self.get_camera().yaw * pi / 180), 0)
        if event.char == 'q':
            self.get_camera().move(-cos(self.get_camera().yaw * pi / 180), -sin(self.get_camera().yaw * pi / 180), 0)
        if event.char == 'z':
            self.get_camera().move(-sin(self.get_camera().yaw * pi / 180), cos(self.get_camera().yaw * pi / 180), 0)
        if event.char == 's':
            self.get_camera().move(sin(self.get_camera().yaw * pi / 180), -cos(self.get_camera().yaw * pi / 180), 0)
        if event.char == 'a':
            self.get_camera().move(0, 0, 1)
        if event.char == 'e':
            self.get_camera().move(0, 0, -1)
        if event.char == 'r':
            self.gui.use(
                WorldScreen.with_(World.load(open(f'{get_env("ASSETS_DIR")}worlds/{self.world.props["file_name"]}.json'
                                                  , mode='r', encoding='utf-8').read())))
        else:
            self.update()

    @property
    def intersections(self):
        return list(
            set([road.paths[0].intersection for road in self.world.roads] + [road.paths[1].intersection for road in
                                                                             self.world.roads]))

    @staticmethod
    def with_(world):
        return type("WorldScreen_Impl", (WorldScreen,), {"world": world})

    def on_leave(self):
        self._stop_thread = True
    
    def build_ground(self):
        ground_offset = random.randint(0, 100000000)
        seed1 = random.randint(0, 100000000)
        seed2 = random.randint(0, 100000000)
    
        for x in range(-20, 20):
            for y in range(-20, 20):
                freq, amp, bias = pi / 8, 10, -9.9
                height00 = improved_noise.noise(x * freq + ground_offset, y * freq) * amp + bias
                height01 = improved_noise.noise(x * freq + ground_offset, (y + 1) * freq) * amp + bias
                height10 = improved_noise.noise((x + 1) * freq + ground_offset, y * freq) * amp + bias
                height11 = improved_noise.noise((x + 1) * freq + ground_offset, (y + 1) * freq) * amp + bias

                face_width = 20
                
                dx00 = improved_noise.noise(x * 1 + seed1, y * 1) * face_width * 20
                dy00 = improved_noise.noise(x * 1 + seed2, y * 1) * face_width * 20
                dx01 = improved_noise.noise(x * 1 + seed1, (y + 1) * 1) * face_width * 20
                dy01 = improved_noise.noise(x * 1 + seed2, (y + 1) * 1) * face_width * 20
                dx10 = improved_noise.noise((x + 1) * 1 + seed1, y * 1) * face_width * 20
                dy10 = improved_noise.noise((x + 1) * 1 + seed2, y * 1) * face_width * 20
                dx11 = improved_noise.noise((x + 1) * 1 + seed1, (y + 1) * 1) * face_width * 20
                dy11 = improved_noise.noise((x + 1) * 1 + seed2, (y + 1) * 1) * face_width * 20
            
                material = Material({"Kd": [0, 150/255, 0], "d": 1})
            
                models = self.get_models()
                obj_pos = Vector3(x * face_width, y * face_width, 0)
            
                triangle1 = Polygon([], {})
                triangle2 = Polygon([], {})
                
                if random.random() < 0.5:
                    triangle1.faces.append(Face([Vertex(Vector3(dx00, dy00, height00), obj_pos),
                                                 Vertex(Vector3(dx01, dy01 + face_width, height01), obj_pos),
                                                 Vertex(Vector3(face_width + dx10, dy10, height10), obj_pos)
                                                 ], material))
                    triangle2.faces.append(Face([Vertex(Vector3(face_width + dx11, face_width + dx11, height11), obj_pos),
                                                 Vertex(Vector3(dx01, face_width + dx01, height01), obj_pos),
                                                 Vertex(Vector3(face_width + dx10, dx10, height10), obj_pos)
                                                 ], material))
                else:
                    triangle1.faces.append(Face([Vertex(Vector3(dx01, face_width + dx01, height01), obj_pos),
                                                 Vertex(Vector3(dx00, dx00, height00), obj_pos),
                                                 Vertex(Vector3(face_width + dx11, face_width + dx11, height11), obj_pos)
                                                 ], material))
                    triangle2.faces.append(Face([Vertex(Vector3(face_width + dx10, dx10, height10), obj_pos),
                                                 Vertex(Vector3(dx00, dx00, height00), obj_pos),
                                                 Vertex(Vector3(face_width + dx11, face_width + dx11, height11), obj_pos)
                                                 ], material))
            
                triangle1.set_camera(self.get_camera())
                triangle2.set_camera(self.get_camera())
            
                models[models._model_id] = triangle1
                models[models._model_id + 1] = triangle2
                models._model_id += 2
