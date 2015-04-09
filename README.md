# pyConnect4: Final Project
## Authors: Kalvin Eng and Nicholas Westbury
## CMPUT 275: Lec B1 / EB1
An implementation of Connect 4 in python's pygame with emphasis on the AI.

## Requirements
- pygame
- python3

## Files
The source code can be found on GitHub: https://github.com/nwestbury/pyConnect4
The files included should be as follows:
    BasePlayer.py (inherited in Player.py, functions that are used in both the Human and AI Classes)
    Player.py (the AI and Human Classes, that have their own play functions)
    board.py (the board containing the pieces)
    main.py (the primary game loop)
    piece.py (the graphic piece class)
    tree.py (the minimax tree)
    README.md (this file, using MarkDown)
    
All files are in full conformity with PEP8.

## Running Connect 4
To run the game, cd to directory of the game and enter `python3 main.py` in
terminal.

To change who plays edit main.py file line 51's player1 and 52's player2
variable to either AI() or Human(). Custom names can be added by giving
argument inside AI("NAME") or Human("NAME"). The following is an example:

         player1 = AI("CPU")
         player2 = Human("Player")

To play again, press the 'r' button on your keyboard.

## Fun Stuff

### bitboard
The board of this game implemented by a 64 bit bitboard. The bitboard
representation is as follows and each of the two players has their own bitboard:
```
        .  .  .  .  .  .  .  TOP
        5 12 19 26 33 40 47
        4 11 18 25 32 39 46
        3 10 17 24 31 38 45
        2  9 16 23 30 37 44
        1  8 15 22 29 36 43
        0  7 14 21 28 35 42  BOTTOM
```
Where each space is a bit, the rest of the spaces that are not shown or '.'
will always be 0.

Using a bitboard representation allows for faster computation times in
calculating the costs and seeing who wins in the game since each board is
represented as a 64 bit number.

### AI

The AI consists of the evaluation function and a graph class. The evalaution
function calculates a cost for each board of a node in the graph.
The graph class stores the possible combinations of boards in a tree-like
structure, where each node is a representation of a possibility of a baord.
To decide a move, the AI moves up each node by depth using a mini-max
algorithm (alternating between max cost of the board and min cost of the
board each depth). The call on the AI's search function allows to either
use normal minimax or minimax with alpha-beta prunning (True by default),
an optimization that allows us to go deeper in the tree.

## Credits

John Tromp's bitboard - http://tromp.github.io/c4/Connect4.java

Evaluating position in bitboard - http://www.gamedev.net/topic/596955-trying-bit-boards-for-connect-4/

Alpha-beta prunning - http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

## To be implemented

- Main menu where you can decide who plays
- Different difficulties of AI (changing depth and modifying evaluation
   function)
- Improved graphics, sound
- More optimizing
