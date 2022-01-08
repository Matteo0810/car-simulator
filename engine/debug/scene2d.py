from random import shuffle

import pygame

from engine.car_ai import AIImpl
from engine.debug.controller import PygameController
from engine.physics import check_collision
from world.car import Car, CarType
from helpers.vector import Vector2
from engine.debug.camera2d import Camera2d
from helpers.dotenv import get_env
from helpers.utils import *


def to_pixel(v, camera):
    return int(v.x / get_env("PIXEL_WIDTH") + get_env("WIDTH") / 2 + camera.x), int(v.y / get_env("PIXEL_WIDTH") + get_env("HEIGHT") / 2 + camera.y)


def map_to_pixel(vl, camera):
    return [to_pixel(v, camera) for v in vl]


class Scene2d:
    def __init__(self, screen: pygame.Surface, world):
        self._world = world
        
        self._user_car = None
        self.reset()
        
        self._screen = screen
        
        self._camera = Camera2d(0, 0)
        self._debug_dots = {}
    
    def clear(self):
        self._screen.fill((255, 255, 255))
    
    def update(self, dt: float):
        self.clear()
        self._render(dt)
        pygame.display.update()
    
    def _render(self, dt):
        for road in self.world.roads:
            points = [
                road.start + Vector2.of_angle((road.end - road.start).angle() - pi / 2) * get_env("ROAD_WIDTH") / 2,
                road.start + Vector2.of_angle((road.end - road.start).angle() + pi / 2) * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() + pi /2) * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() - pi / 2) * get_env("ROAD_WIDTH") / 2,
            ]
            
            pygame.draw.polygon(self._screen, (100, 100, 100), map_to_pixel(points, self._camera))

            points = [
                road.start + Vector2.of_angle((road.end - road.start).angle() - pi / 2) / 4 + (road.end - road.start).normalize() * get_env("ROAD_WIDTH") / 2,
                road.start + Vector2.of_angle((road.end - road.start).angle() + pi / 2) / 4 + (road.end - road.start).normalize() * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() + pi / 2) / 4 - (road.end - road.start).normalize() * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() - pi / 2) / 4 - (road.end - road.start).normalize() * get_env("ROAD_WIDTH") / 2,
            ]

            pygame.draw.polygon(self._screen, (200, 200, 200), map_to_pixel(points, self._camera))

        for car in self._world.cars:
            car.ai.pre_tick(dt)
        for car in self._world.cars:
            car.tick(dt)
        for car1 in self._world.cars:
            for car2 in self._world.cars:
                if car1 is not car2:
                    check_collision(car1, car2, dt)
        for car in self._world.cars:
            car.update_last_position(dt)
            car.reconstruct()
            
            points = [wheel.position for wheel in car.wheels]
            
            pygame.draw.polygon(self._screen, car.color, map_to_pixel(points, self._camera))

        debug_dots = self._debug_dots.copy()
        for dot, l in debug_dots.items():
            if l[0] < 0.2:
                l[0] += dt
                pygame.draw.rect(self.screen, l[1], (to_pixel(dot, self._camera) + (2, 2)))
        
        #if len(world.car.A) > 0:
        #    print(max(world.car.A.items(), key=lambda t: t[1]))
        #for x, y in world.car.A.items():
        #    pygame.draw.rect(self.screen, (0, 0, 0), (x, y * 100, 1, 1))
    
    def reset(self):
        self._world.cars.clear()
        
        blue_controls = {
            "z": pygame.K_UP,
            "q": pygame.K_LEFT,
            "s": pygame.K_DOWN,
            "d": pygame.K_RIGHT
        }
        
        green_car = Car(self._world, Vector2(0, -30), 0, CarType(None, 2.2, 5, 1, (0, 255, 0), 30))
        green_car.ai = PygameController(green_car, self, 300, 150)
        
        colors = [(0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        shuffle(colors)
        
        cars = [green_car]
        
        for i in range(5):
            path = self._world.roads[i].paths[0 if i != 3 and i != 4 else 1]  # Vector2(random.random() * 200 - 100, random.random() * 100)
            car = Car(self._world, path.start, path.direction.angle(),
                           CarType(None, 2.2, 5, 1, colors[i], 10))
            car.ai = AIImpl(path, car)
            cars.append(car)

        self._world.cars.extend(cars)
        
        self._user_car = self._world.cars[0]
    
    def add_debug_dot(self, position, color=(255, 0, 0)):
        self._debug_dots[position] = [0, color]
    
    screen = property_get("screen")
    user_car = property_get("user_car")
    world = property_get("world")
