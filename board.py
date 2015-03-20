#!/usr/bin/python3

import pygame
from main import WINDOW_DIMENSIONS
from pygame.locals import *

# y=100
class Board:
    def __init__(self, width=7, height=6, tokensize=80):

        self.TOKENSIZE = tokensize
        self.WIDTH = width*tokensize
        self.HEIGHT = height*tokensize
        self.COLOR = (0, 0, 255)
        self.XMARG = (WINDOW_DIMENSIONS[0] - self.WIDTH) // 2
        self.YMARG = WINDOW_DIMENSIONS[1] // 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, (self.XMARG, self.YMARG,
                                              self.WIDTH, self.HEIGHT))
