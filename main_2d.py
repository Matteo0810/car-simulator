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
    
    last_frame = time()
    
    current_thread = threading.current_thread()
    
    class PFThread(threading.Thread):
        def __init__(self, car):
            super().__init__()
            self._car = car
        
        def run(self):
            sleep(0.1)
            while current_thread.is_alive() and self._car in world.cars:
                if isinstance(self._car.ai, AIImpl):
                    self._car.ai.pathfinding(scene)
                sleep(0)

    scene = Scene2d(screen, world, PFThread)
    
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
        scene.update(dt*0.8)

        last_frame = frame_start
        
        sleep(max(0., 0.001 - (time() - frame_start)))


if __name__ == '__main__':
    main()
