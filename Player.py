from BasePlayer import BasePlayer
import random


class Human (BasePlayer):
    def __init__(self):
        BasePlayer.__init__(self, "Player", False)

    def detectColClick(self, board, mousepos):
        if board.RECT.collidepoint(mousepos):  # if click is inside the board
            colNumber = (mousepos[0]-board.XMARG)//board.TOKENSIZE
            return colNumber
        return -1

    def play(self, board, mouseloc):
        return self.detectColClick(board, mouseloc)


class AI (BasePlayer):
    def __init__(self):
        BasePlayer.__init__(self, "CPU", True)

    def play(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        possibleBits = self.getCoordinates(myBoard | oppBoard)

        forcedCols = []
        for colbitTuple in possibleBits:
            tempMyBoard = self.setNthBit(myBoard, colbitTuple[1])
            tempOppBoard = self.setNthBit(oppBoard, colbitTuple[1])

            if board.hasWon(tempMyBoard):
                return colbitTuple[0]
            elif board.hasWon(tempOppBoard):
                forcedCols.append(colbitTuple[0])

        if forcedCols:
            print("Forced Columns:", forcedCols)
            return forcedCols[0]
        return random.randint(0, 6)
