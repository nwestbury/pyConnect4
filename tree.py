#!/usr/bin/python3


class graph:
    def __init__(self, myBoard, oppBoard):
        # initiate the first/root node to be at depth 0 and pointing to itself
        rootNode = node(myBoard, oppBoard, 0, -1, -1)
        self.root = rootNode

    def getMove(self):
        """
        This function simply returns the column from the minimax graphs's top
        values. In the case there is more than one column equally-well rated,
        we will randomly return one of them (we didn't bother seeding the rand
        since we'd prefer results are reproducible).
        """

        bestvalue = self.root.value
        rootChildren = self.root.children

        print("Best   value :", bestvalue)
        print("Column values:", rootChildren)

        bestColumns = [c.col for c in rootChildren if c.value == bestvalue]

        if bestColumns:
            if len(bestColumns) > 1:
                # return the column closest to the center, if they are all equ
                return min(bestColumns, key=lambda x: 3-x)
            else:
                return bestColumns[0]

        raise Exception("Failed to find best value")

    def construct_tree(self, b, ai, parentNode, myBoard, oppBoard, depth):
        """
        Likely the most complex function, this builds the tree of possibilities
        by brute forcing through all possible configurations up to a given depth
        (maxDepth). It works by getting the legal locations of where a place can
        be placed, and setting those bits (equivalent to placing a token). Once
        the board is either won or the max depth is reached, we evaluate the
        board. When the function pops out, it creates the value of the parent
        node based on its children values (maxmizing the values if we are
        playing or minimizing if the opponent is playing). On a high level, we
        are presuming both players will play the optimal moves and we want to
        maxmize our reward and minimize the opponent's rewards. We alternate
        back and forth from maximizing and minizming the reward after the
        lowest tree values have been filled.

        tl;dr This function fills a minimax tree.

        The function runs in O(7^n) (n=depth), but the true expansion is
        considerably less than this after the move # + depth >= 4, because we
        stop branches where there is a win and all seven columns are not
        necessarily available.

        """
        bMyTurn = (depth % 2 == 1)
        maxDepth = 5

        possibleBits = ai.get_legal_locations(myBoard | oppBoard)
        childrenNodes = []

        for colbitTuple in possibleBits:
            won = False
            col = colbitTuple[0]

            if bMyTurn:  # it's my turn, so add to my board
                tmpMyBoard = ai.setNthBit(myBoard, colbitTuple[1])
                tmpOppBoard = oppBoard
                won = b.hasWon(tmpMyBoard)
            else:  # it's the oppnent's turn, so we simulate their move
                tmpMyBoard = myBoard
                tmpOppBoard = ai.setNthBit(oppBoard, colbitTuple[1])
                won = b.hasWon(tmpOppBoard)

            myNode = node(tmpMyBoard, tmpOppBoard, depth, parentNode, col)

            # stop expanding the branch if the game is won | max depth = reached
            if won or depth == maxDepth:
                myNode.value = ai.evalCost(b, tmpOppBoard, tmpMyBoard, bMyTurn)
            else:
                self.construct_tree(b, ai, myNode,
                                    tmpMyBoard, tmpOppBoard, depth+1)
                myNode.setValueFromChildren()

            childrenNodes.append(myNode)

        parentNode.children = childrenNodes
        parentNode.setValueFromChildren()


class node:
    def __init__(self, myBoard, oppBoard, depth, parentNode, col, value=None):
        self.myBoard = myBoard
        self.oppBoard = oppBoard
        self.value = value
        self.depth = depth
        if depth == 0:  # if the node is the root
            self.parent = self  # set the parent node to itself
        else:
            self.parent = parentNode
        self.children = []
        self.col = col

    def setValueFromChildren(self):
        """
        Get the value of a node based on its children, minimizing if value if
        it's the opponent turn or maxmizing if it's before my turn.
        """
        if self.children and self.value is None:
            if self.depth % 2:
                self.value = min(c.value for c in self.children)
            else:
                self.value = max(c.value for c in self.children)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, node):
        return self.value == node.value

    def __lt___(self, node):
        return self.value < node.value

    def __gt__(self, node):
        return self.value > node.value
