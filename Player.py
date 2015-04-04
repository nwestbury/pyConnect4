from BasePlayer import BasePlayer
import tree


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

    def heuristic(self, board, myBoard, oppBoard, bMyTurn):
        winReward = 10000
        OppCost3Row = 1000 if bMyTurn else 100
        MyCost3Row = 100
        OppCost2Row = 100 if bMyTurn else 10
        MyCost2Row = 10
        if board.hasWon(myBoard):
            return winReward
        elif board.hasWon(oppBoard):
            return -winReward
        else:
            # self.printBoard(myBoard)
            # self.printBoard(oppBoard)
            threeScore = self.checkForNInRow(myBoard, 3)*MyCost3Row -\
                self.checkForNInRow(oppBoard, 3)*OppCost3Row
            twoScore = self.checkForNInRow(myBoard, 2)*MyCost2Row -\
                self.checkForNInRow(oppBoard, 2)*OppCost2Row
            # self.printBoard(myBoard)
            # print("SCORE", threeScore, twoScore)
            return threeScore + twoScore

    def checkForNInRow(self, bitboard, n):
        """
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

    """def recursive_search(self, b, myBoard, oppBoard, col, costs, depth):
        if depth > 5:
            return

        possibleBits = self.get_legal_locations(myBoard | oppBoard)

        for colbitTuple in possibleBits:
            tmpMyB = self.setNthBit(myBoard, colbitTuple[1])
            tmpOppB = self.setNthBit(oppBoard, colbitTuple[1])

            costs[col] += self.heuristic(b, tmpMyB, depth, True)
            costs[col] += self.heuristic(b, tmpOppB, depth, False)
            self.recursive_search(b, tmpMyB, tmpOppB, col, costs, depth+1)"""

    def testSearch(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        g = tree.graph(myBoard, oppBoard)  # minimax graph
        rootNode = g.root
        g.construct_tree(board, self, rootNode, myBoard, oppBoard, 1)
        test = g.getMove()
        print("CHOSE", test)

        return test
        # return the key with the highest score, which is the best column
        # return max(costs, key=costs.get)
    """def search(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        possibleBits = self.get_legal_locations(myBoard | oppBoard)
        costs = dict()

        for colbitTuple in possibleBits:
            col = colbitTuple[0]
            costs[col] = -1000
            tmpMyB = self.setNthBit(myBoard, colbitTuple[1])
            tmpOppB = self.setNthBit(oppBoard, colbitTuple[1])

            self.recursive_search(board, tmpMyB, tmpOppB, col, costs, 2)

        print("TEST", costs)

        # return the key with the highest score, which is the best column
        return max(costs, key=costs.get)"""

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
            print("Forced Columns:", forcedCols)
            return forcedCols[0]
        return -1

    def play(self, board):
        """forcedColumn = self.forced_moves(board)
        if forcedColumn > -1:
            return forcedColumn"""

        return self.testSearch(board)

    """def play(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        possibleBits = self.getCoordinates(myBoard | oppBoard)

        forcedCols = []  # cols needed to block your opponent if you cannot win
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
        return random.randint(0, 6)"""
