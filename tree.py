class graph:
    def __init__(self, myBoard, oppBoard):
        rootNode = node(myBoard, oppBoard, 0, -1, -1)
        self.root = rootNode

    def getChildrenValues(self, node):
        for child in node.children:
            self.getChildrenValues(child)
            child.setValueFromChildren()

    def getMove(self):
        self.getChildrenValues(self.root)
        self.root.setValueFromChildren()
        bestvalue = self.root.value

        print("Best Value:", bestvalue)

        print("Root children: %s" % self.root.children)
        for child in self.root.children:
            print("Col%d children: %s" % (child.col, child.children))

        self.root.setValueFromChildren()

        for child in self.root.children:
            if child.value == bestvalue:
                return child.col

        raise Exception("Failed to find best value")

    def construct_tree(self, b, ai, parentNode, myBoard, oppBoard, depth):
        bMyTurn = (depth % 2 == 1)
        if depth == 4:
            parentNode.value = ai.heuristic(b, myBoard, oppBoard, bMyTurn)
            return

        possibleBits = ai.get_legal_locations(myBoard | oppBoard)
        childrenNodes = []

        for colbitTuple in possibleBits:
            won = False
            col = colbitTuple[0]

            if bMyTurn:  # odd means it's my board
                tmpMyBoard = ai.setNthBit(myBoard, colbitTuple[1])
                tmpOppBoard = oppBoard
                won = b.hasWon(tmpMyBoard)
            else:  # it's the oppnent's turn, so we simulate their moves
                tmpMyBoard = myBoard
                tmpOppBoard = ai.setNthBit(oppBoard, colbitTuple[1])
                won = b.hasWon(tmpOppBoard)

            myNode = node(tmpMyBoard, tmpOppBoard, depth, parentNode, col)

            if won:
                myNode.value = ai.heuristic(b, tmpMyBoard, tmpOppBoard, bMyTurn)
            else:
                self.construct_tree(b, ai, myNode,
                                    tmpMyBoard, tmpOppBoard, depth+1)
            childrenNodes.append(myNode)

        parentNode.children = childrenNodes


class node:
    def __init__(self, myBoard, oppBoard, depth, parentNode, col, value=0):
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
        if self.children:
            if self.depth % 2 == 0:
                self.value = max(c.value for c in self.children)
            else:
                self.value = min(c.value for c in self.children)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, node):
        return self.value == node.value

    def __lt___(self, node):
        return self.value < node.value

    def __gt__(self, node):
        return self.value > node.value
