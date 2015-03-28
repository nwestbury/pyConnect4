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
        board.BITBOARDS[p] |= (1 << (x*7 + y))

    def getNthBit(self, num, n):
        return (num >> n) & 1

    def setNthBit(self, num, n):
        return num | (1 << n)

    def printBoard(self, board):
        print(">" * 14)
        for i in range(5, -1, -1):
            row = ""
            for x in range(7):
                row += str(self.getNthBit(board, i+x*7)) + " "
            print(row)
        print("<" * 14)

    def getCoordinates(self, overall):
        listOfCoords = []
        for i in range(7):
            for x in range(i*7, i*7+6):
                if not self.getNthBit(overall, x):
                    listOfCoords.append((i, x))
                    break
        return listOfCoords
