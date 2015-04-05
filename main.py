#!/usr/bin/python3

import pygame
import sys
import board
from pygame.locals import QUIT, KEYUP, MOUSEBUTTONUP, K_ESCAPE
from Player import Human, AI

FPS = 30  # this isn't an intense game, so 30 frames per second is good enough
WINDOW_DIMENSIONS = (640, 640)  # Width and height of the pygame window
BACKGROUND_COLOUR = (100, 100, 100)  # A shade of gray


def quit():
    """
    This function is called on a clean quit.
    """
    pygame.quit()
    sys.exit()


def main():
    """
    The main function from which everything else is ran
    """
    global FPS, WINDOW_DIMENSIONS, BACKGROUND_COLOUR

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption('pyConnect4')

    background = pygame.Surface(WINDOW_DIMENSIONS)
    background = background.convert()
    background.fill(BACKGROUND_COLOUR)

    FPSCLOCK = pygame.time.Clock()

    screen.blit(background, (0, 0))

    player1 = Human()
    player2 = AI()
    gameBoard = board.Board(player1, player2)

    count = 0  # count for time elapsed
    isDone = False

    while not isDone:
        board.draw_header(gameBoard.COUNT1, gameBoard.COUNT2, screen)  # DrawTop
        board.draw_footer(gameBoard.TURN, count, screen)  # DrawBottom
        gameBoard.draw(screen)  # draw the main game board
        pygame.display.flip()  # update the screen
        count += FPSCLOCK.tick(FPS)

        if gameBoard.isAITurn():
            isDone = gameBoard.play()
            pygame.event.clear()  # ignore clicks while the CPU was "thinking"

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or \
               (event.type == KEYUP and event.key == K_ESCAPE):
                quit()
            elif event.type == MOUSEBUTTONUP and event.button == 1 and\
                    not gameBoard.isAITurn():
                mousepos = pygame.mouse.get_pos()
                isDone = gameBoard.play(mousepos)
                print("CLICK AT:", mousepos)

    if isDone == 1:
        print("Player %d (%s) wins!!!" %
              (gameBoard.TURN + 1, gameBoard.PLAYERS[gameBoard.TURN]))
    else:
        print("Draw!")

    while True:
        gameBoard.draw(screen)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or \
               (event.type == KEYUP and event.key == K_ESCAPE):
                quit()

if __name__ == "__main__":
    main()
