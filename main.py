#!/usr/bin/python3

import pygame
import sys
import board
from pygame.locals import QUIT, KEYUP, MOUSEBUTTONUP, K_ESCAPE

FPS = 30
WINDOW_DIMENSIONS = (640, 640)  # Width and height of the pygame window
BACKGROUND_COLOUR = (100, 100, 100)  # A shade of gray


def quit():
    pygame.quit()
    sys.exit()


def main():
    global FPS, WINDOW_DIMENSIONS, BACKGROUND_COLOUR

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption('pyConnect4')

    background = pygame.Surface(WINDOW_DIMENSIONS)
    background = background.convert()
    background.fill(BACKGROUND_COLOUR)

    FPSCLOCK = pygame.time.Clock()

    screen.blit(background, (0, 0))

    gameBoard = board.Board()

    while True:
        gameBoard.draw(screen)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or \
               (event.type == KEYUP and event.key == K_ESCAPE):
                quit()
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                colNum = gameBoard.detectColClick(mousepos)
                isWin = gameBoard.placeToken(colNum)
                if isWin:
                    print("Player", gameBoard.TURN + 1, "wins!!!")
                    quit()
                print("CLICK AT:", mousepos)

if __name__ == "__main__":
    main()
