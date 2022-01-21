import os
from time import time, sleep
import json

import pygame

from helpers.dotenv import dotenv, get_env
from engine.debug.scene2d import Scene2d
from world.world import World


def main():
    dotenv()
    
    pygame.init()
    screen = pygame.display.set_mode((get_env("WIDTH"), get_env("HEIGHT")))

    json_world = json.loads(open("assets/worlds/forest.json", mode='r').read())
    world = World.load(json_world)
    
    last_frame = time()

    scene = Scene2d(screen, world)
    scene.start_pf_threads()
    scene.camera.set_zoom(2)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    scene.reset()
                    scene.start_pf_threads()

        frame_start = time()
        dt = (frame_start - last_frame)
        scene.update(dt*0.8)

        last_frame = frame_start
        
        sleep(max(0., 0.001 - (time() - frame_start)))


if __name__ == '__main__':
    main()
