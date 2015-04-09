#!/usr/bin/python3

from pygame import gfxdraw


class Piece:
    def __init__(self, boardx, boardy, board, tokensize=80):
        margin = 10  # margin on both sides of token
        self.radius = tokensize//2 - margin
        self.BOARDX = boardx
        self.BOARDY = boardy
        self.X = board.XMARG + boardx * tokensize + self.radius + margin
        self.Y = board.YMARG + boardy * tokensize + self.radius + margin
        # Player 1 (P1) has color red, P2 has color yellow, and empty is white
        self.COLORS = [(255, 255, 255), (255, 0, 0), (255, 255, 0)]
        self.STATUS = 0  # A status of 0 indicates no piece, 1 is P1, 2 is P2

    def draw(self, screen):
        """
        Argument:
        screen : the surface to draw on

        This function draws an antialiased circle at the X,Y of the piece.
        Unfortuately, antialiased filled circles don't exsist so we draw
        the antialiased outline before drawing the filled inside, as recommneded
        by the offical docs (otherwise the circles look horrendously ugly).

        """
        cur_color = self.COLORS[self.STATUS]
        gfxdraw.aacircle(screen, self.X, self.Y, self.radius, cur_color)
        gfxdraw.filled_circle(screen, self.X, self.Y, self.radius, cur_color)

    def setColorToPlayer(self, player):
        """
        Argument:
        player : an integer that is either 1 or 2 that speifies the current
        player, this will change the color when it is printed to the screen.

        """
        self.STATUS = player

    def __repr__(self):
        return str(self.STATUS)
