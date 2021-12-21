from sys import exit
from time import time, sleep

from helpers.dotenv import dotenv, get_env
from engine.debug.scene2d import Scene2d
from world.world import World

import pygame
import json


def main():
    dotenv()
    
    pygame.init()
    screen = pygame.display.set_mode((get_env("WIDTH"), get_env("HEIGHT")))

    json_world = json.loads(open("world/assets/world.json", mode='r').read())
    world = World.load(json_world)

    scene = Scene2d(screen, world)
    
    last_frame = time()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        
        dt = (time() - last_frame)*2
        scene.controller.tick(dt)
        scene.update(dt)
        
        last_frame = time()
        sleep(0.01)


if __name__ == '__main__':
    main()
