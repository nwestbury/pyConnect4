#!/usr/bin/python3

import pygame
import sys
from pygame.locals import *

FPS = 30
WINDOW_DIMENSIONS = (640, 480)  # Width and height of the pygame window


def main():
    global FPS, WINDOW_DIMENSIONS

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption('pyConnect4')

    background = pygame.Surface(WINDOW_DIMENSIONS)
    background = background.convert()
    background.fill((100, 100, 100))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or \
               (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
