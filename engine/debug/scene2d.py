import random
from random import shuffle

import pygame

from engine.ai.car_ai import AIImpl
from engine.debug.controller import PygameController
from engine.physics import check_collision
from world.car import Car, CarType
from helpers.vector import Vector2
from engine.debug.camera2d import Camera2d
from helpers.dotenv import get_env
from helpers.utils import *
from world.intersection import IntersectionType

pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 20)


def to_pixel(v, camera):
    return int(v.x / get_env("PIXEL_WIDTH") / camera.zoom + get_env("WIDTH") / 2 + camera.x), int(
        v.y / get_env("PIXEL_WIDTH") / camera.zoom + get_env("HEIGHT") / 2 + camera.y)


def map_to_pixel(vl, camera):
    return [to_pixel(v, camera) for v in vl]


class Scene2d:
    def __init__(self, screen: pygame.Surface, world, debug=False):
        self._world = world
        self._screen = screen
        self._debug = debug

        self._user_car = None
        self.reset()

        self._camera = Camera2d(0, 0)
        self._debug_dots = {}

    def clear(self):
        self._screen.fill((20, 60, 0))

    def update(self, dt: float):
        self.clear()
        self._render(dt)
        pygame.display.update()

        if pygame.key.get_pressed()[pygame.K_u]:
            car2 = random.choice(self._world.cars)
            self._user_car.ai = AIImpl(random.choice(random.choice(self._world.roads).paths), self._user_car)
            self._user_car.ai.start_thread(self)

            if isinstance(car2.ai, AIImpl):
                car2.ai.stop_thread()

            car2.ai = PygameController(car2, self, 100, 50)

            self._user_car = car2

    def _render(self, dt):
        for road in self.world.roads:
            points = [
                road.start + Vector2.of_angle((road.end - road.start).angle() - pi / 2) * get_env("ROAD_WIDTH") / 2,
                road.start + Vector2.of_angle((road.end - road.start).angle() + pi / 2) * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() + pi / 2) * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() - pi / 2) * get_env("ROAD_WIDTH") / 2,
            ]

            pygame.draw.polygon(self._screen, (100, 100, 100), map_to_pixel(points, self._camera))

            points = [
                road.start + Vector2.of_angle((road.end - road.start).angle() - pi / 2) / 4 + (
                            road.end - road.start).normalize() * get_env("ROAD_WIDTH") / 2,
                road.start + Vector2.of_angle((road.end - road.start).angle() + pi / 2) / 4 + (
                            road.end - road.start).normalize() * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() + pi / 2) / 4 - (
                            road.end - road.start).normalize() * get_env("ROAD_WIDTH") / 2,
                road.end + Vector2.of_angle((road.end - road.start).angle() - pi / 2) / 4 - (
                            road.end - road.start).normalize() * get_env("ROAD_WIDTH") / 2,
            ]

            pygame.draw.polygon(self._screen, (200, 200, 200), map_to_pixel(points, self._camera))

            if not self._debug:
                for path in road.paths:
                    if path.intersection.ligths_type == IntersectionType.LIGHTS:
                        if path.intersection.is_green(path):
                            pygame.draw.rect(self.screen, (0, 255, 0), (
                                        to_pixel(path.end - path.direction * get_env("ROAD_WIDTH"), self._camera) + (
                                4, 4)))
                        else:
                            pygame.draw.rect(self.screen, (255, 0, 0), (
                                        to_pixel(path.end - path.direction * get_env("ROAD_WIDTH"), self._camera) + (
                                4, 4)))

            if self._debug:
                self.screen.blit(DEFAULT_FONT.render(str(road.id), True, (0, 255, 0)),
                                 to_pixel(road.end / 2 + road.start / 2, self._camera))

        if self._debug:
            for intersection in self.intersections:
                self.screen.blit(DEFAULT_FONT.render(str(intersection.id), True, (120, 0, 120)), to_pixel(
                    sum(inbound.path.end for inbound in intersection.inbounds) / len(intersection.inbounds),
                    self._camera))
                for i in range(-1, len(intersection.inbounds) - 1):
                    i1 = intersection.inbounds[i]
                    i2 = intersection.inbounds[i + 1]
                    pygame.draw.line(self._screen, (255, 100, 0),
                                     to_pixel(i1.path.end - i1.path.direction * get_env("ROAD_WIDTH") / 2,
                                              self._camera),
                                     to_pixel(i2.path.end - i2.path.direction * get_env("ROAD_WIDTH") / 2,
                                              self._camera))

        for intersection in self.intersections:
            intersection.tick(self.world, dt)

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

        # if len(world.car.A) > 0:
        #    print(max(world.car.A.items(), key=lambda t: t[1]))
        # for x, y in world.car.A.items():
        #    pygame.draw.rect(self.screen, (0, 0, 0), (x, y * 100, 1, 1))

    def reset(self):
        if self._debug:
            return

        self._world.cars.clear()

        blue_controls = {
            "z": pygame.K_UP,
            "q": pygame.K_LEFT,
            "s": pygame.K_DOWN,
            "d": pygame.K_RIGHT
        }

        green_car = Car(self._world, Vector2(0, -50), 0, CarType("car", 2.2, 5, 1, (0, 255, 0), 15))
        green_car.ai = PygameController(green_car, self, 100, 50)

        blue_car = Car(self._world, Vector2(0, -40), 0, CarType("car", 2.2, 5, 1, (0, 0, 255), 15))
        blue_car.ai = PygameController(blue_car, self, 100, 50, blue_controls)
        # (0, 0, 255),
        colors = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        shuffle(colors)

        cars = [green_car, blue_car]  # green_car

        for i in range(3):
            path = self._world.roads[i].paths[
                0 if i != 3 and i != 4 else 1]  # Vector2(random.random() * 200 - 100, random.random() * 100)
            car = Car(self._world, path.start, path.direction.angle(),
                      CarType("car", 2.2, 5, 1, colors[i], 10))
            car.ai = AIImpl(path, car)
            cars.append(car)

        self._world.cars.extend(cars)

        self._user_car = self._world.cars[0]

    def start_pf_threads(self):
        for car in self._world.cars:
            if isinstance(car.ai, AIImpl):
                car.ai.start_thread(self)

    def add_debug_dot(self, position, color=(255, 0, 0)):
        self._debug_dots[position] = [0, color]

    @property
    def intersections(self):
        return list(
            set([road.paths[0].intersection for road in self.world.roads] + [road.paths[1].intersection for road in
                                                                             self.world.roads]))

    screen = property_get("screen")
    user_car = property_get("user_car")
    world = property_get("world")
    camera = property_get("camera")
