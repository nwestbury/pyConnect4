#!/usr/bin/python3

import pygame
from main import WINDOW_DIMENSIONS
from piece import Piece


class Board:
    def __init__(self, width=7, height=6, tokensize=80):

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

    def placeToken(self, col):
        """
        Argument:
        col : the column number by default an int between [0,6] where a token
        is requested to be placed.

        Return: True if the placed token wins the game, False otherwise
        """
        if col < 0:  # invalid column
            return False
        pieceCol = self.PIECES[col]
        for piece in pieceCol:
            if not piece.STATUS:  # if the column has an empty space
                piece.setColorToPlayer(self.TURN + 1)
                return self.endTurn()
        return False  # if the column is full, return False

    def detectColClick(self, mousepos):
        if self.RECT.collidepoint(mousepos):  # if the click is inside the board
            colNumber = (mousepos[0]-self.XMARG)//self.TOKENSIZE
            return colNumber
        return -1

    def checkWin(self, p):
        """
        Argument:
        p : an integer that is either 1 or 2 that speifies the current
        player, since we only need to check for a win after a token was placed.
        """
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                # check horizontals
                if x < (self.WIDTH - 3):
                    if all(self.PIECES[x+i][y].STATUS == p for i in range(4)):
                        return True
                # check / diagonals
                if x < (self.WIDTH - 3) and y < (self.HEIGHT - 3):
                    if all(self.PIECES[x+i][y+i].STATUS == p for i in range(4)):
                        return True
                # check \ diagonals
                if x < (self.WIDTH - 3) and y > 2:
                    if all(self.PIECES[x+i][y-i].STATUS == p for i in range(4)):
                        return True
                # check verticals
                if y < (self.HEIGHT - 3):
                    if all(self.PIECES[x][y+i].STATUS == p for i in range(4)):
                        return True
        return False

    def endTurn(self):
        """
        This function is called at the end of every turn. It returns True on win
        False otherwise
        """
        if self.checkWin(self.TURN + 1):
            return True
        self.TURN = not self.TURN
        return False
