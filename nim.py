"""
nim.py
created on: 01/15/2020
created by: Anna Branam
last modified: 02/12/2020


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
        
    def checkWin(self):
        coins = 0
        for stack in self.board.getStacks():
            coins+= sum(coin.inStack() for coin in stack.getCoins())#count coins that are still on the board
        return coins == 0 or coins == 1#if there are no coins on the board, the game is over
    
    def quit(self):
        pygame.quit()
        sys.exit()
            
    def play(self):
        ###INITS###
        ##################################
        self.genBoard()
        self.graphics = Graphics(self.board)
        turn = 0
        currentPlayer = self.players[0]
        ##################################

        self.graphics.displayBoard()#display the board

        ###MAIN GAME LOOP###
        #####################################################
        while (not self.checkWin()):
            #start the current player's turn#
            #########################
            if not currentPlayer.onTurn():
                self.graphics.showPlayer(currentPlayer.name)
                currentPlayer.startTurn()
                self.graphics.displayBoard()#display the board
            #########################
            
            #check for events#
            ##########################################
            e = pygame.event.get()
            for event in e:
                #check for exit#
                if event.type == pygame.QUIT:
                    self.quit()

                #Check for key Presses#
                elif event.type ==pygame.KEYDOWN:
                    KeyDownEvent(self.board, self.graphics, event).handle(currentPlayer)
                    break
                
                #Check for mouse clicks#
                elif event.type == pygame.MOUSEBUTTONUP and event.button ==1:#Left mouse button pressed
                    CoinClickEvent(self.board, self.graphics, event).handle(currentPlayer)
                    break
            ##########################################
                
            #check for next turn
            if not currentPlayer.onTurn():
                turn+=1
                currentPlayer = self.players[turn%len(self.players)]
            pygame.display.flip()
        ###end of main game loop###
        #####################################################
        #display win
        self.graphics.displayWin(currentPlayer.name)
        return

############################################################################
#main function
############################################################################

if __name__=="__main__":
    g = Game()
    g.play()
    
