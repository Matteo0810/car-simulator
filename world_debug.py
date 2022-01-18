import os
from time import time, sleep
import json

import pygame

from helpers.dotenv import dotenv, get_env
from engine.debug.scene2d import Scene2d
from world.world import World


def update_scene(screen):
    json_world = json.loads(open("world/assets/worlds/forest.json", mode='r').read())
    world = World.load(json_world)
    scene = Scene2d(screen, world, debug=True)
    scene.camera.set_zoom(2)
    return scene


def main():
    dotenv()
    
    pygame.init()
    screen = pygame.display.set_mode((get_env("WIDTH"), get_env("HEIGHT")))

    scene = update_scene(screen)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    scene = update_scene(screen)
        scene.update(0.1)

if __name__ == '__main__':
    main()
