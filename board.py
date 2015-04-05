#!/usr/bin/python3

import pygame
import time
from main import WINDOW_DIMENSIONS
from piece import Piece


def draw_header(player_moves, cpu_moves, surface):
    """
    Draw the header of the game
     - Title
     - Player move count

    """
    # erase the surface to be written to
    pygame.draw.rect(surface, (100, 100, 100), (0, 0,
                                                WINDOW_DIMENSIONS[0],
                                                WINDOW_DIMENSIONS[1] // 7))

    # Set default system font, size 72
    title_font = pygame.font.Font(None, 72)

    title = title_font.render("Connect 4", True, (255, 255, 255))
    surface.blit(title,
                 (WINDOW_DIMENSIONS[0] // 16,
                  WINDOW_DIMENSIONS[1] // 18))

    moves_font = pygame.font.Font(None, 24)

    cpu_title = moves_font.render("CPU moves:", True, (255, 255, 255))
    cpu_move = moves_font.render(str(cpu_moves), True, (255, 255, 255))

    moves_x = WINDOW_DIMENSIONS[0] - WINDOW_DIMENSIONS[0] // 11
    surface.blit(cpu_move, (moves_x,  WINDOW_DIMENSIONS[1] // 15.5))
    surface.blit(cpu_title, (moves_x - WINDOW_DIMENSIONS[0] // 6,
                             WINDOW_DIMENSIONS[1] // 15.5))

    player_title = moves_font.render("Player moves:", True, (255, 255, 255))
    player_move = moves_font.render(str(player_moves), True, (255, 255, 255))

    # 29 is added to y coordinate for \n since font size is 24
    surface.blit(player_move, (moves_x, WINDOW_DIMENSIONS[1] // 18 + 29))
    surface.blit(player_title, (moves_x - WINDOW_DIMENSIONS[0] // 5.25,
                                WINDOW_DIMENSIONS[1] // 18 + 29))


def draw_footer(turn, timer, surface):
    """
    Draw the footer of the game
     - Current player playing
     - Running time of game

    """
    # erase surface to be written to
    pygame.draw.rect(surface, (100, 100, 100),
                     (0, WINDOW_DIMENSIONS[1] - (WINDOW_DIMENSIONS[1] // 12),
                      WINDOW_DIMENSIONS[0], WINDOW_DIMENSIONS[1] // 12))

    footer_font = pygame.font.Font(None, 24)

    time_title = footer_font.render("Time Elapsed:", True, (255, 255, 255))

    # convert seconds to time
    seconds = time.strftime('%H:%M:%S', time.gmtime(timer // 1000))

    surface.blit(time_title,
                 (WINDOW_DIMENSIONS[0] // 16,
                  WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1] // 18))

    time_count = footer_font.render(seconds, True, (255, 255, 255))
    surface.blit(time_count,
                 (WINDOW_DIMENSIONS[0] // 4.1,
                  WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1] // 18))

    turn_title = footer_font.render("Turn:", True, (255, 255, 255))

    turn_x = WINDOW_DIMENSIONS[0] - (WINDOW_DIMENSIONS[0]) // 4.7

    surface.blit(turn_title,
                 (turn_x,
                  WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1] // 18))

    # decide to display who's turn
    if not turn:
        turn_text = "CPU"
    else:
        turn_text = "Player"

    turn = footer_font.render(turn_text, True, (255, 255, 255))
    surface.blit(turn,
                 (turn_x + WINDOW_DIMENSIONS[0] // 14,
                  WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1] // 18))


class Board:
    def __init__(self, p1, p2, tokensize=80):

        width, height = 7, 6  # for now, the width and height will remain fixed

        self.TOKENSIZE = tokensize
        self.BOARDWIDTH = width*tokensize
        self.BOARDHEIGHT = height*tokensize
        self.WIDTH = width
        self.HEIGHT = height
        self.COLOR = (0, 0, 255)
        self.XMARG = (WINDOW_DIMENSIONS[0] - self.BOARDWIDTH) // 2
        self.YMARG = WINDOW_DIMENSIONS[1] // 6
        self.RECT = pygame.Rect(self.XMARG, self.YMARG,
                                self.BOARDWIDTH, self.BOARDHEIGHT)
        self.TURN = 0

        self.COUNT1 = 0  # player 1 moves
        self.COUNT2 = 0  # player 2 moves

        self.PLAYERS = (p1, p2)
        self.BITBOARDS = [0, 0]

        self.PIECES = []
        for piecex in range(width):
            colTokens = []
            for piecey in reversed(range(height)):
                t = Piece(piecex, piecey, self)
                colTokens.append(t)
            self.PIECES.append(colTokens)

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, self.RECT)
        for col in self.PIECES:
            for piece in col:
                piece.draw(screen)

    def play(self, mouseloc=(0, 0)):
            chosenCol = -1
            player = self.PLAYERS[self.TURN]
            if player.isAI:
                chosenCol = player.play(self)
            else:
                chosenCol = player.play(self, mouseloc)

            if chosenCol >= 0:
                return self.placeToken(chosenCol)

            return False

    def placeToken(self, col):
        """
        Argument:
        col : the column number by default an int between [0,6] where a token
        is requested to be placed.

        Return: 1 if the placed token wins the game 2 if draw, 0 otherwise
        """
        if col < 0:  # invalid column
            return False

        pieceCol = self.PIECES[col]
        y = 0
        for piece in pieceCol:
            if not piece.STATUS:  # if the column has an empty space
                piece.setColorToPlayer(self.TURN + 1)
                self.PLAYERS[self.TURN].flipBit(self, self.TURN, col, y)
                return self.endTurn()
            y += 1
        return False  # if the column is full, return False

    def hasWon(self, bitboard):
        # taken from http://stackoverflow.com/q/7033165/1524592
        y = bitboard & (bitboard >> 6)
        if (y & (y >> 2 * 6)):  # check \ diagonal
            return True
        y = bitboard & (bitboard >> 7)
        if (y & (y >> 2 * 7)):  # check horizontal
            return True
        y = bitboard & (bitboard >> 8)
        if (y & (y >> 2 * 8)):  # check / diagonal
            return True
        y = bitboard & (bitboard >> 1)
        if (y & (y >> 2)):  # check vertical
            return True
        return False

    def hasDrawn(self, overall_bitboard):
        return (overall_bitboard & 18446464815071240256) == 18446464815071240256

    def endTurn(self):
        """
        This function is called at the end of every turn. It returns 1 on win
        2 on draw
        False otherwise
        """
        if self.hasWon(self.BITBOARDS[self.TURN]):
            return 1

        if self.hasDrawn(self.BITBOARDS[0] | self.BITBOARDS[1]):
            return 2

        self.TURN = not self.TURN

        # add to player move count
        if self.TURN:
            self.COUNT2 += 1
        else:
            self.COUNT1 += 1

        return False

    def isAITurn(self):
        return self.PLAYERS[self.TURN].isAI
