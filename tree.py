#!/usr/bin/python3


class graph:
    def __init__(self, myBoard, oppBoard, maxDepth):
        # initiate the first/root node to be at depth 0 and pointing to itself
        rootNode = Node(myBoard, oppBoard, 0, -1, -1)
        self.root = rootNode
        self.maxDepth = maxDepth  # the max depth to consider moves

    def getMove(self):
        """
        This function simply returns the column from the minimax graphs's top
        values. In the case there is more than one column equally-well rated,
        we will the one closest to the center.

        """

        bestvalue = self.root.value
        rootChildren = self.root.children

        print("Best   value :", bestvalue)
        print("Column values:", rootChildren)

        bestColumns = [c.col for c in rootChildren if c.value == bestvalue]

        print("COLS", bestColumns)

        if bestColumns:
            if len(bestColumns) > 1:
                # return the column closest to the center, if they are all
                # equal
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

        The function runs in O(7^d) (d=maxDepth), but the true expansion is
        considerably less than this after the move # + depth >= 4, because we
        stop branches where there is a win and all seven columns are not
        necessarily available.

        """
        bMyTurn = (depth % 2 == 1)

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

            myNode = Node(tmpMyBoard, tmpOppBoard, depth, parentNode, col)

            # stop expanding the branch if the game is won | max depth = reached
            if won or depth == self.maxDepth:
                myNode.value = ai.evalCost(b, tmpOppBoard, tmpMyBoard, bMyTurn)
            else:
                self.construct_tree(b, ai, myNode,
                                    tmpMyBoard, tmpOppBoard, depth+1)
                myNode.setValueFromChildren()

            childrenNodes.append(myNode)

        parentNode.children = childrenNodes
        parentNode.setValueFromChildren()

    def createNodeChildren(self, ai, node):
        """
        This function will look at all the possible locations you can play
        pieces and create their respective nodes. After this list of nodes is
        created it is added to the inital's node class variable children.
        """
        bMyTurn = node.depth % 2
        possibleBits = ai.get_legal_locations(node.myBoard | node.oppBoard)
        childrenNodes = []
        for colbitTuple in possibleBits:
            col = colbitTuple[0]
            if bMyTurn:
                tmpMyBoard = ai.setNthBit(node.myBoard, colbitTuple[1])
                tmpOppBoard = node.oppBoard
            else:
                tmpMyBoard = node.myBoard
                tmpOppBoard = ai.setNthBit(node.oppBoard, colbitTuple[1])
            childNode = Node(tmpMyBoard, tmpOppBoard, node.depth+1, node, col)
            childrenNodes.append(childNode)
        node.children = childrenNodes

    def alphabeta(self, b, ai, node, depth, alpha, beta):
        """
        Constructs the tree using alphabeta, this is quite similar to the raw
        minimax used in the construct tree, however it is considerably faster
        because it removes branches that cannot be used. Simply put, it takes
        advantage of the minimax's attribute to maxmize and then minimize the
        nodes' values. For instance, if you have a bottom value of 5 and find
        a value of -100 at the bottom, you can ignore the entire branch because
        you know it will be minizmized before reaching the top.

        On my laptop, this equates to an increase from depth 5 to 7 for a max
        wait of ~2 seconds over non-optimized minimax.
        """
        isTurn = node.depth % 2 == 0  # if it's the AI's turn, we should maxmize
        if depth == 0 or node.depth == self.maxDepth:
            if node.value is None:
                node.value = ai.evalCost(b, node.myBoard, node.oppBoard, isTurn)
            return node.value

        self.createNodeChildren(ai, node)
        if isTurn:
            v = float('-inf')
            for child in node.children:
                v = max(v, self.alphabeta(b, ai, child, depth-1, alpha, beta))
                alpha = max(alpha, v)
                if node.value is None or alpha > node.value:
                    node.value = alpha
                if beta <= alpha:
                    node.value = None
                    break
            return v
        else:
            v = float('inf')
            for child in node.children:
                v = min(v, self.alphabeta(b, ai, child, depth-1, alpha, beta))
                beta = min(beta, v)
                if node.value is None or beta < node.value:
                    node.value = beta
                if beta <= alpha:
                    node.value = None
                    break
            return v


class Node:
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
            return self.value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, node):
        return self.value == node.value

    def __lt___(self, node):
        return self.value < node.value

    def __gt__(self, node):
        return self.value > node.value
