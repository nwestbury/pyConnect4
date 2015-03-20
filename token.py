#!/usr/bin/python3

import pygame
from main import WINDOW_DIMENSIONS
from pygame.locals import *


class Token:
    def __init__(self, boardx, boardy, tokensize=80):

        self.BOARDX = boardx
        self.BOARDY = boardy
        self.X = boardx
        self.Y = boardy

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, (self.XMARG, self.YMARG,
                                              self.WIDTH, self.HEIGHT))
