"""
nim.py
created on: 01/15/2020
created by: Anna Branam
last modified: 02/13/2020


Nim is a game that consists of stacks of coins
the numbers of stacks and the number of coins in each stack varies
each player can take any number of coins from a single stack
the last player to remove a coin loses
"""

############################################################################
#imports
############################################################################
import sys
import random
import nim_exceptions as exceptions
from nim_mechanics import *
from nim_graphics import *
from nim_board import *
############################################################################
#classes
############################################################################

class Game():
    def __init__(self):
        self.players = [Player("Player 1"), Player("Player 2")]
        self.board, self.graphics = None, None

    def genBoard(self, stacks=[]):
        if stacks == []:#If no coins are specified, randomize
            for i in range(random.randrange(2, 6)):
                stacks.append(random.randrange(1, 6))
        self.board = Board(stacks)
        
    def play(self):
        ###INITS###
        self.genBoard()
        self.graphics = Graphics(self.board)

        self.graphics.displayBoard()#display the board
        currentPlayer = Runner(self.board, self.graphics, self.players).run()#main game loop
        
        #display win
        self.graphics.displayWin(currentPlayer.name)
        return

############################################################################
#main function
############################################################################

if __name__=="__main__":
    g = Game()
    g.play()
    
