#!/usr/bin/python3

import pygame
import sys
import board
from pygame.locals import QUIT, KEYUP, MOUSEBUTTONUP, K_ESCAPE, K_r
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


def playAgain():
    """
    This function checks to see if a new game wants to be played at the end.
    """
    while True:
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or \
               (event.type == KEYUP and event.key == K_ESCAPE):
                quit()
            elif event.type == KEYUP and event.key == K_r:
                main()


def main():
    """
    The main function from which everything else is run
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

    # Change the following two lines to add a Human() or an AI()
    # The parameter is a string for the name of the player.
    player1 = AI("CPU 1")
    player2 = AI("CPU 2")
    gameBoard = board.Board(player1, player2)

    count = 0  # count for time elapsed
    isDone = False

    while not isDone:
        # draw header and footer
        board.draw_header(gameBoard.PLAYERS, gameBoard.COUNT1,
                          gameBoard.COUNT2, screen)
        board.draw_footer(gameBoard.TURN, gameBoard.PLAYERS, count, screen)
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

    gameBoard.draw(screen)

    message_font = pygame.font.Font(None, 100)
    message_pos = screen.get_rect().centerx

    if isDone == 1:
        message_text = str(gameBoard.PLAYERS[gameBoard.TURN]) + " Wins!"
    else:
        message_text = "Draw!"

    message = message_font.render(message_text, True, (160, 160, 169))
    message_pos = message.get_rect()
    message_pos.centerx = screen.get_rect().centerx
    message_pos.centery = screen.get_rect().centery
    screen.blit(message, message_pos)

    pygame.display.flip()  # update the screen

if __name__ == "__main__":
    main()
    playAgain()
