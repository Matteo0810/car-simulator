import os
import threading
from time import time, sleep
import json

import pygame

from engine.car_ai import AIImpl
from helpers.dotenv import dotenv, get_env
from engine.debug.scene2d import Scene2d
from world.world import World


def main():
    dotenv()
    
    pygame.init()
    screen = pygame.display.set_mode((get_env("WIDTH"), get_env("HEIGHT")))

    json_world = json.loads(open("world/assets/world.json", mode='r').read())
    world = World.load(json_world)

    scene = Scene2d(screen, world)
    
    last_frame = time()

    current_thread = threading.current_thread()
    pathfinding_thread = threading.Thread()
    
    def pathfinding_thread_run():
        while current_thread.is_alive():
            sleep(0.1)
            for car in world.cars:
                if isinstance(car.ai, AIImpl):
                    car.ai.pathfinding(scene)

    pathfinding_thread.__dict__["lock"] = threading.Lock()
    pathfinding_thread.run = pathfinding_thread_run
    pathfinding_thread.start()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    scene.reset()

        frame_start = time()
        dt = (frame_start - last_frame)
        scene.update(dt/1)

        last_frame = frame_start
        sleep(max(0., 0.001 - (time() - frame_start)))


if __name__ == '__main__':
    main()
