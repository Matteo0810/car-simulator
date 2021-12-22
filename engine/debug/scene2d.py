from engine.debug.controller import Controller
from world.car import Car, CarType
from helpers.vector import Vector2
from engine.debug.camera2d import Camera2d
from helpers.dotenv import get_env
from helpers.utils import *
from world.road import Road
from world.world import World

import pygame


class Scene2d:
    def __init__(self, screen: pygame.Surface, world):
        self._world = world

        self._user_car = None
        self.reset()
        
        self._screen = screen
        
        self._camera = Camera2d(0, 0)
        self._controller = Controller(self)
    
    def clear(self):
        self._screen.fill((255, 255, 255))
    
    def update(self, dt: float):
        self.clear()
        self._render(dt)
        pygame.display.update()
    
    def _render(self, dt):
        for road in self.world.roads:
            points = [
                road.start + Vector2.of_angle((road.end - road.start).angle() - pi/2) * get_env("ROAD_WIDTH") / 2,
                road.start + Vector2.of_angle((road.end - road.start).angle() + pi/2) * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() + pi/2) * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() - pi/2) * get_env("ROAD_WIDTH") / 2,
            ]
            
            points = [(int(p.x + get_env("WIDTH") / 2 + self._camera.x), int(p.y + get_env("HEIGHT") / 2 + self._camera.y)) for p in points]
            pygame.draw.polygon(self._screen, (100, 100, 100), points)
        
        for car in self._world.cars:
            car.tick(self.world, dt)
            
            points = (wheel.position for wheel in car._wheels)
            points = [(int(p.x + get_env("WIDTH") / 2 + self._camera.x), int(p.y + get_env("HEIGHT") / 2 + self._camera.y)) for p in points]
            
            pygame.draw.polygon(self._screen, car.color, points)
    
    def reset(self):
        self._world.cars.clear()
        
        self._world.cars.extend([Car(Vector2(0, 0), 0, CarType(None, 10, 20, 1, (0, 255, 0), 25)),
                Car(Vector2(50, 0), 0, CarType(None, 10, 20, 1, (0, 0, 255), 25))])
        
        self._user_car = self._world.cars[0]
    
    screen = property_get("screen")
    user_car = property_get("user_car")
    controller = property_get("controller")
    world = property_get("world")
