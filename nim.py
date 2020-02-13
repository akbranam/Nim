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
import nim_mechanics
import nim_graphics
import nim_board
############################################################################
#classes
############################################################################

class Game():
    def __init__(self):
        self.players = [nim_mechanics.Player("Player 1"), nim_mechanics.Player("Player 2")]
        self.board, self.graphics = None, None

    def genBoard(self, stacks=[]):
        if stacks == []:#If no coins are specified, randomize
            for i in range(random.randrange(2, 6)):
                stacks.append(random.randrange(1, 6))
        self.board = nim_board.Board(stacks)
    def menu(self):
        pass
    def play(self):
        ###INITS###
        self.genBoard()
        self.graphics = nim_graphics.Graphics(self.board)

        self.graphics.displayBoard()#display the board
        turn = nim_mechanics.Runner(self.board, self.graphics, self.players).run()#main game loop
        
        #display win
        self.graphics.displayWin(self.players[turn%len(self.players)].getName())
        
        return

############################################################################
#main function
############################################################################

if __name__=="__main__":
    g = Game()
    g.play()
    
