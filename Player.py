#!/usr/bin/python3

from BasePlayer import BasePlayer
import tree


class Human (BasePlayer):
    def __init__(self, name="Human"):
        BasePlayer.__init__(self, name, False)

    def detectColClick(self, board, mousepos):
        if board.RECT.collidepoint(mousepos):  # if click is inside the board
            colNumber = (mousepos[0]-board.XMARG)//board.TOKENSIZE
            return colNumber
        return -1

    def play(self, board, mouseloc):
        return self.detectColClick(board, mouseloc)


class AI (BasePlayer):
    def __init__(self, name="CPU"):
        BasePlayer.__init__(self, name, True)

    def evaluate3(self, oppBoard, myBoard):
        """
        Returns the number of possible 3 in a rows in bitboard format.

        Running time: O(1)

        http://www.gamedev.net/topic/596955-trying-bit-boards-for-connect-4/

        """
        inverseBoard = ~(myBoard | oppBoard)
        rShift7MyBoard = myBoard >> 7
        lShift7MyBoard = myBoard << 7
        rShift14MyBoard = myBoard >> 14
        lShit14MyBoard = myBoard << 14
        rShift16MyBoard = myBoard >> 16
        lShift16MyBoard = myBoard << 16
        rShift8MyBoard = myBoard >> 8
        lShift8MyBoard = myBoard << 8
        rShift6MyBoard = myBoard >> 6
        lShift6MyBoard = myBoard << 6
        rShift12MyBoard = myBoard >> 12
        lShift12MyBoard = myBoard << 12

        # check _XXX and XXX_ horizontal
        result = inverseBoard & rShift7MyBoard & rShift14MyBoard\
            & (myBoard >> 21)

        result |= inverseBoard & rShift7MyBoard & rShift14MyBoard\
            & lShift7MyBoard

        result |= inverseBoard & rShift7MyBoard & lShift7MyBoard\
            & lShit14MyBoard

        result |= inverseBoard & lShift7MyBoard & lShit14MyBoard\
            & (myBoard << 21)

        # check XXX_ diagonal /
        result |= inverseBoard & rShift8MyBoard & rShift16MyBoard\
            & (myBoard >> 24)

        result |= inverseBoard & rShift8MyBoard & rShift16MyBoard\
            & lShift8MyBoard

        result |= inverseBoard & rShift8MyBoard & lShift8MyBoard\
            & lShift16MyBoard

        result |= inverseBoard & lShift8MyBoard & lShift16MyBoard\
            & (myBoard << 24)

        # check _XXX diagonal \
        result |= inverseBoard & rShift6MyBoard & rShift12MyBoard\
            & (myBoard >> 18)

        result |= inverseBoard & rShift6MyBoard & rShift12MyBoard\
            & lShift6MyBoard

        result |= inverseBoard & rShift6MyBoard & lShift6MyBoard\
            & lShift12MyBoard

        result |= inverseBoard & lShift6MyBoard & lShift12MyBoard\
            & (myBoard << 18)

        # check for _XXX vertical
        result |= inverseBoard & (myBoard << 1) & (myBoard << 2)\
            & (myBoard << 3)

        return result

    def evaluate2(self, oppBoard, myBoard):
        """
        Returns the number of possible 2 in a rows in bitboard format.

        Running time: O(1)

        """
        inverseBoard = ~(myBoard | oppBoard)
        rShift7MyBoard = myBoard >> 7
        rShift14MyBoard = myBoard >> 14
        lShift7MyBoard = myBoard << 7
        lShift14MyBoard = myBoard << 14
        rShift8MyBoard = myBoard >> 8
        lShift8MyBoard = myBoard << 8
        lShift16MyBoard = myBoard << 16
        rShift16MyBoard = myBoard >> 16
        rShift6MyBoard = myBoard >> 6
        lShift6MyBoard = myBoard << 6
        rShift12MyBoard = myBoard >> 12
        lShift12MyBoard = myBoard << 12

        # check for _XX
        result = inverseBoard & rShift7MyBoard & rShift14MyBoard
        result |= inverseBoard & rShift7MyBoard & rShift14MyBoard
        result |= inverseBoard & rShift7MyBoard & lShift7MyBoard

        # check for XX_
        result |= inverseBoard & lShift7MyBoard & lShift14MyBoard

        # check for XX / diagonal
        result |= inverseBoard & lShift8MyBoard & lShift16MyBoard

        result |= inverseBoard & rShift8MyBoard & rShift16MyBoard
        result |= inverseBoard & rShift8MyBoard & rShift16MyBoard
        result |= inverseBoard & rShift8MyBoard & lShift8MyBoard

        # check for XX \ diagonal
        result |= inverseBoard & rShift6MyBoard & rShift12MyBoard
        result |= inverseBoard & rShift6MyBoard & rShift12MyBoard
        result |= inverseBoard & rShift6MyBoard & lShift6MyBoard
        result |= inverseBoard & lShift6MyBoard & lShift12MyBoard

        # check for _XX vertical
        result |= inverseBoard & (myBoard << 1) & (myBoard << 2) \
            & (myBoard << 2)

        return result

    def evaluate1(self, oppBoard, myBoard):
        """
        Returns the number of possible 1 in a rows in bitboard format.

        Running time: O(1)

        Diagonals are skipped since they are worthless.

        """
        inverseBoard = ~(myBoard | oppBoard)
        # check for _X
        result = inverseBoard & (myBoard >> 7)

        # check for X_
        result |= inverseBoard & (myBoard << 7)

        # check for _X vertical
        result |= inverseBoard & (myBoard << 1)

        return result

    def bitboardBits(self, i):
        """"
        Returns the number of bits in a bitboard (7x6).

        Running time: O(1)

        Help from: http://stackoverflow.com/q/9829578/1524592

        """
        i = i & 0xFDFBF7EFDFBF  # magic number to mask to only legal bitboard
        # positions (bits 0-5, 7-12, 14-19, 21-26, 28-33, 35-40, 42-47)
        i = (i & 0x5555555555555555) + ((i & 0xAAAAAAAAAAAAAAAA) >> 1)
        i = (i & 0x3333333333333333) + ((i & 0xCCCCCCCCCCCCCCCC) >> 2)
        i = (i & 0x0F0F0F0F0F0F0F0F) + ((i & 0xF0F0F0F0F0F0F0F0) >> 4)
        i = (i & 0x00FF00FF00FF00FF) + ((i & 0xFF00FF00FF00FF00) >> 8)
        i = (i & 0x0000FFFF0000FFFF) + ((i & 0xFFFF0000FFFF0000) >> 16)
        i = (i & 0x00000000FFFFFFFF) + ((i & 0xFFFFFFFF00000000) >> 32)

        return i

    def evalCost(self, b, oppBoard, myBoard, bMyTurn):
        """
        Returns cost of each board configuration.

        winning is a winning move
        blocking is a blocking move

        Running time: O(7n)

        """
        winReward = 9999999
        OppCost3Row = 1000
        MyCost3Row = 3000
        OppCost2Row = 500
        MyCost2Row = 500
        OppCost1Row = 100
        MyCost1Row = 100

        if b.hasWon(oppBoard):
            return -winReward
        elif b.hasWon(myBoard):
            return winReward

        get3Win = self.evaluate3(oppBoard, myBoard)
        winning3 = self.bitboardBits(get3Win) * MyCost3Row

        get3Block = self.evaluate3(myBoard, oppBoard)
        blocking3 = self.bitboardBits(get3Block) * -OppCost3Row

        get2Win = self.evaluate2(oppBoard, myBoard)
        winning2 = self.bitboardBits(get2Win) * MyCost2Row

        get2Block = self.evaluate2(myBoard, oppBoard)
        blocking2 = self.bitboardBits(get2Block) * -OppCost2Row

        get1Win = self.evaluate1(oppBoard, myBoard)
        winning1 = self.bitboardBits(get1Win) * MyCost1Row

        get1Block = self.evaluate1(myBoard, oppBoard)
        blocking1 = self.bitboardBits(get1Block) * -OppCost1Row

        return winning3 + blocking3 + winning2 + blocking2\
            + winning1 + blocking1

    def search(self, board, use_alphabeta=True):
        """
        Construct the minimax tree, and get the best move based off the root.

        You have two options to build the tree:
            if use_alphabeta is True:
                alpha beta will be used to construct the tree
            otherwise:
                raw minimax will be used to construct the tree (it may be
            required to lower the maxDepth because it will be slower).
        """
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        maxDepth = 7

        g = tree.graph(myBoard, oppBoard, maxDepth)  # minimax graph

        if use_alphabeta:
            g.alphabeta(board, self, g.root, maxDepth,
                        float('-inf'), float('inf'))
        else:
            g.construct_tree(board, self, g.root, myBoard, oppBoard, 1)

        return g.getMove()

    def forced_moves(self, board):
        """
        If placing a token can win immediately, return that column.
        Otherwise, if you can block your opponent immediately, return
        one of those column(s).
        """

        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        possibleBits = self.get_legal_locations(myBoard | oppBoard)

        forcedCols = []  # cols needed to block your opponent if you cannot win
        for colbitTuple in possibleBits:
            tempMyBoard = self.setNthBit(myBoard, colbitTuple[1])
            tempOppBoard = self.setNthBit(oppBoard, colbitTuple[1])

            if board.hasWon(tempMyBoard):
                return colbitTuple[0]
            elif board.hasWon(tempOppBoard):
                forcedCols.append(colbitTuple[0])

        if forcedCols:
            return forcedCols[0]
        return -1

    def play(self, board):
        """
        Returns the column to place the piece in.
        """

        forcedColumn = self.forced_moves(board)  # if there is a forced move
        if forcedColumn > -1:
            return forcedColumn  # play it

        return self.search(board)  # otherwise, search the tree
