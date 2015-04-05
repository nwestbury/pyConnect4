#!/usr/bin/python3

from BasePlayer import BasePlayer
import tree


class Human (BasePlayer):
    def __init__(self):
        BasePlayer.__init__(self, "Human", False)

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

    def evaluate3(self, oppBoard, myBoard):
        """
        Returns the number of possible 3 in a rows in bitboard format.

        Running time: O(1)

        http://www.gamedev.net/topic/596955-trying-bit-boards-for-connect-4/

        """

        inverseBoard = ~(myBoard | oppBoard)

        # check _XXX and XXX_ horizontal

        result = inverseBoard & (myBoard >> 7) & (myBoard >> 14)\
            & (myBoard >> 21)

        result |= inverseBoard & (myBoard >> 7) & (myBoard >> 14)\
            & (myBoard << 7)

        result |= inverseBoard & (myBoard >> 7) & (myBoard << 7)\
            & (myBoard << 14)

        result |= inverseBoard & (myBoard << 7) & (myBoard << 14)\
            & (myBoard << 21)

        # check XXX_ diagonal /
        result |= inverseBoard & (myBoard >> 8) & (myBoard >> 16)\
            & (myBoard >> 24)

        result |= inverseBoard & (myBoard >> 8) & (myBoard >> 16)\
            & (myBoard << 8)

        result |= inverseBoard & (myBoard >> 8) & (myBoard << 8)\
            & (myBoard << 16)

        result |= inverseBoard & (myBoard << 8) & (myBoard << 16)\
            & (myBoard << 24)

        # check _XXX diagonal \
        result |= inverseBoard & (myBoard >> 6) & (myBoard >> 12)\
            & (myBoard >> 18)

        result |= inverseBoard & (myBoard >> 6) & (myBoard >> 12)\
            & (myBoard << 6)

        result |= inverseBoard & (myBoard >> 6) & (myBoard << 6)\
            & (myBoard << 12)

        result |= inverseBoard & (myBoard << 6) & (myBoard << 12)\
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

        # check for _XX
        result = inverseBoard & (myBoard >> 7) & (myBoard >> 14)\
            & (myBoard >> 14)

        result |= inverseBoard & (myBoard >> 7) & (myBoard >> 14)
        result |= inverseBoard & (myBoard >> 7) & (myBoard << 7) \
            & (myBoard << 7)

        # check for XX_
        result |= inverseBoard & (myBoard << 7) & (myBoard << 14) \
            & (myBoard << 14)

        # check for XX / diagonal
        result |= inverseBoard & (myBoard << 8) & (myBoard << 16) \
            & (myBoard << 16)

        result |= inverseBoard & (myBoard >> 8) & (myBoard >> 16) \
            & (myBoard >> 16)
        result |= inverseBoard & (myBoard >> 8) & (myBoard >> 16)
        result |= inverseBoard & (myBoard >> 8) & (myBoard << 8) \
            & (myBoard << 8)

        # check for XX \ diagonal
        result |= inverseBoard & (myBoard >> 6) & (myBoard >> 12) \
            & (myBoard >> 12)

        result |= inverseBoard & (myBoard >> 6) & (myBoard >> 12)
        result |= inverseBoard & (myBoard >> 6) & (myBoard << 6) \
            & (myBoard << 6)
        result |= inverseBoard & (myBoard << 6) & (myBoard << 12) \
            & (myBoard << 12)

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

        http://stackoverflow.com/questions/9829578/fast-way-of-counting-bits-in-python
        """

        i = i & 0xFDFBF7EFDFBF  # magic number to mask to only legal bit
        # board positions (bits 0-5, 7-12, 14-19, 21-26, 28-33, 35-40, 42-47)
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

        winReward = 999999999
        OppCost3Row = 1000  # if bMyTurn else 500
        MyCost3Row = 10000
        OppCost2Row = 100  # if bMyTurn else 100
        MyCost2Row = 50
        OppCost1Row = 0  # if bMyTurn else 10
        MyCost1Row = 0

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

    def checkForNInRow(self, bitboard, n):
        """
        This function returns the amount of n in a row found in the board.
        It has been deprecated by the much faster binary functions above which
        are optimized for n = 1, 2, and 3.

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
        counter = 0
        for col_num in range(7):
            low_col = col_num*7
            top_col = low_col + 6
            for bb_index in range(low_col, top_col):
                bHorizontalSpace = n+col_num <= 7
                bVerticalSpace = bb_index+n <= top_col
                bVerticalDownSpace = bb_index-n+1 >= low_col

                # check right horiontal
                if bHorizontalSpace and\
                        all((self.getNthBit(bitboard, k)
                             for k in range(bb_index, (bb_index+7*n), 7))):
                    counter += 1
                # check top vertical
                if bVerticalSpace and\
                    all((self.getNthBit(bitboard, k)
                        for k in range(bb_index, (bb_index+n)))):
                    counter += 1
                # check / vertical
                if bHorizontalSpace and bVerticalSpace and\
                    all((self.getNthBit(bitboard, k)
                        for k in range(bb_index, (bb_index+8*n), 8))):
                    counter += 1
                # check \ vertical
                if bHorizontalSpace and bVerticalDownSpace and\
                    all((self.getNthBit(bitboard, k)
                        for k in range(bb_index, (bb_index+6*n), 6))):
                    counter += 1
        return counter

    def search(self, board):
        """
        Construct the minimax tree, and get the best move based off the root.
        """
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        g = tree.graph(myBoard, oppBoard)  # minimax graph
        g.construct_tree(board, self, g.root, myBoard, oppBoard, 1)

        return g.getMove()

    def forced_moves(self, board):
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
        forcedColumn = self.forced_moves(board)  # if there is a forced move
        if forcedColumn > -1:
            return forcedColumn  # play it

        return self.search(board)  # otherwise, search the tree
