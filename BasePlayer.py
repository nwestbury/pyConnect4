#!/usr/bin/python3


class BasePlayer:
    def __init__(self, name, isAI):
        """
        BasePlayer is inherited by Player.py for Human and AI, it contains
        variables and functions useful to both classes.

        name is the name of the player (e.g. "CPU", "Human")
        isAI is a boolean where or not the player is an AI

        bitboard is a bitboard representation of the board for the given player
        The bitboard representation is like this:
        .  .  .  .  .  .  .  TOP
        5 12 19 26 33 40 47
        4 11 18 25 32 39 46
        3 10 17 24 31 38 45
        2  9 16 23 30 37 44
        1  8 15 22 29 36 43
        0  7 14 21 28 35 42  BOTTOM

        """
        self.name = name
        self.isAI = isAI

    def __repr__(self):
        return str(self.name)

    def flipBit(self, board, p, x, y):
        """
        Flip the bit at the x/y location.
        """
        board.BITBOARDS[p] |= (1 << (x*7 + y))

    def getNthBit(self, num, n):
        """
        Get the nth bit in the bitboard (0 or 1).
        """
        return (num >> n) & 1

    def setNthBit(self, num, n):
        """
        Set the nth bit in the bitboard to 1.
        """
        return num | (1 << n)

    def printBoard(self, board):
        """
        Print the bit board for a single player

        """
        print(">" * 14)
        for i in range(5, -1, -1):  # iterate backwards from 5 to 0.
            row = " ".join(str(self.getNthBit(board, i+x*7)) for x in range(7))
            print(row)
        print("<" * 14)

    def get_legal_locations(self, overall_bitboard):
        """
        Argument:
            overall_bitboard: the combined bitboard for both players (b1 | b2).
            One needs to combine the boards in order to find the top location
            (and check if its empty for a token).

        This function returns a list of tuples for every location that a piece
        could be placed (max of 7). The tuple has two items. The first is the
        column # (0-6) and the second is the bit index for the bitboard (0-42).
        It will returns an empty list when the board is full.

        .  .  .  .  .  .  .  TOP
        5 12 19 26 33 40 47
        4 11 18 25 32 39 46
        3 10 17 24 31 38 45
        2  9 16 23 30 37 44
        1  8 15 22 29 36 43
        0  7 14 21 28 35 42  BOTTOM

        """
        listOfCoords = []
        for i in range(7):  # for every column
            for x in range(i*7, i*7+6):  # for each cell in col, from bot to top
                if not self.getNthBit(overall_bitboard, x):  # get the 1st empty
                    listOfCoords.append((i, x))
                    break
        return listOfCoords

    def get_legal_board(self, overall_bitboard):
        """
        Takes as an argument a combined bitboard for the opponent and player
        and returns a bitboard with all the valid locations set to one.
        """
        board = 0
        for i in range(7):
            for x in range(i*7, i*7+6):
                if not self.getNthBit(overall_bitboard, x):
                    board |= (1 << x)
                    break
        return board
