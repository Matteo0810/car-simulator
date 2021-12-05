from engine.debug.controller import Controller
from world.car import Car, CarModel
from pygame.math import Vector2
from engine.debug.camera2d import Camera2d
from helpers.dotenv import get_env
from helpers.utils import *
from world.road import Road

import pygame


class Scene2d:
    def __init__(self, screen: pygame.Surface):
        self._cars = [Car(self, Vector2(0, 0), 0, CarModel("default", (10, 20), 1, (0, 255, 0)))]
        self._user_car = self._cars[0]
        
        self._roads = [Road(Vector2(-50, -30), Vector2(50, -30), 34, None, None)]
        
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
        for road in self._roads:
            points = [
                road.start + unit_vector(angle_of(road.end - road.start) - pi) * road.width / 2,
                road.start + unit_vector(angle_of(road.end - road.start) + pi) * road.width / 2,
                road.end + unit_vector(angle_of(road.end - road.start) + pi) * road.width / 2,
                road.end + unit_vector(angle_of(road.end - road.start) - pi) * road.width / 2,
            ]
            
            points = [(int(p.x + get_env("WIDTH") / 2 + self._camera.x), int(p.y + get_env("HEIGHT") / 2 + self._camera.y)) for p in points]
            pygame.draw.polygon(self._screen, (100, 100, 100), points)
            
        for car in self._cars:
            car.tick(dt)
            
            points = (wheel.position for wheel in car._wheels)
            points = [(int(p.x + get_env("WIDTH") / 2 + self._camera.x), int(p.y + get_env("HEIGHT") / 2 + self._camera.y)) for p in points]
            
            pygame.draw.polygon(self._screen, car.color, points)
    
    screen = property_get("screen")
    user_car = property_get("user_car")
    controller = property_get("controller")
