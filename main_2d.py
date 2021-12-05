from sys import exit
from time import time, sleep

from helpers.dotenv import dotenv, get_env
from engine.debug.scene2d import Scene2d

import pygame

dotenv()

pygame.init()
screen = pygame.display.set_mode((get_env("WIDTH"), get_env("HEIGHT")))

scene = Scene2d(screen)

if __name__ == '__main__':
    last_frame = time()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            else:
                scene.controller.handle(event)
        
        dt = time() - last_frame
        scene.controller.tick(dt)
        scene.update(dt)
        
        last_frame = time()
        sleep(0.01)
